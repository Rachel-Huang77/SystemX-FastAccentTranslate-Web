from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from app.api.v1.deps import require_admin
from app.models.user import User
from app.models.conversation import Conversation
from app.models.transcript import Transcript
from app.schemas.admin import (
    UserListQuery,
    UserResponse,
    UserDetailResponse,
    UserListResponse,
    CreateUserRequest,
    UpdateUserRequest,
    ResetPasswordRequest,
    BatchDeleteRequest,
)
from app.core.security import hash_password
from tortoise.expressions import Q
import math

router = APIRouter(prefix="/admin", tags=["admin"])


# ============ 获取用户列表 ============

@router.get("/users", response_model=dict)
async def get_users(
    page: int = Query(default=1, ge=1, description="页码"),
    limit: int = Query(default=20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(default=None, description="搜索关键词"),
    role: Optional[str] = Query(default=None, description="角色过滤"),
    sort_by: str = Query(default="created_at", description="排序字段"),
    sort_order: str = Query(default="desc", description="排序方向"),
    admin_user: User = Depends(require_admin)
):
    """
    获取用户列表
    - 支持分页
    - 支持搜索（用户名或邮箱）
    - 支持角色过滤
    - 支持排序
    """
    # 构建查询
    query = User.all()

    # 搜索过滤
    if search:
        query = query.filter(
            Q(username__icontains=search) | Q(email__icontains=search)
        )

    # 角色过滤
    if role:
        query = query.filter(role=role)

    # 获取总数
    total = await query.count()

    # 排序
    if sort_order == "desc":
        sort_by = f"-{sort_by}"
    query = query.order_by(sort_by)

    # 分页
    offset = (page - 1) * limit
    users = await query.offset(offset).limit(limit)

    # 序列化（移除密码字段）
    user_list = [
        UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login,
        )
        for user in users
    ]

    # 分页信息
    total_pages = math.ceil(total / limit)

    return {
        "success": True,
        "data": {
            "users": [user.dict() for user in user_list],
            "pagination": {
                "total": total,
                "page": page,
                "pageSize": limit,
                "totalPages": total_pages,
            }
        }
    }


# ============ 获取用户详情 ============

@router.get("/users/{user_id}", response_model=dict)
async def get_user_detail(
    user_id: str,
    admin_user: User = Depends(require_admin)
):
    """
    获取用户详细信息
    - 包含用户基本信息
    - 包含统计数据（会话数、对话数）
    """
    # 查询用户
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 查询统计数据
    conversation_count = await Conversation.filter(user_id=user_id).count()
    transcript_count = await Transcript.filter(
        conversation__user_id=user_id
    ).count()

    # 构建响应
    user_detail = UserDetailResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login,
        statistics={
            "total_conversations": conversation_count,
            "total_transcripts": transcript_count,
            "last_activity": user.last_login,
        }
    )

    return {
        "success": True,
        "data": user_detail.dict()
    }


# ============ 创建用户 ============

@router.post("/users", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: CreateUserRequest,
    admin_user: User = Depends(require_admin)
):
    """
    创建新用户
    - 验证用户名唯一性
    - 验证邮箱唯一性
    - 验证密码强度
    - 哈希密码
    """
    # 检查用户名是否存在
    if await User.exists(username=data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "USERNAME_EXISTS",
                "message": "用户名已存在",
                "field": "username"
            }
        )

    # 检查邮箱是否存在
    if await User.exists(email=data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "EMAIL_EXISTS",
                "message": "邮箱已被注册",
                "field": "email"
            }
        )

    # 创建用户
    user = await User.create(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
        is_active=True,
    )

    return {
        "success": True,
        "data": UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=None,
        ).dict(),
        "message": "用户创建成功"
    }


# ============ 更新用户信息 ============

@router.put("/users/{user_id}", response_model=dict)
async def update_user(
    user_id: str,
    data: UpdateUserRequest,
    admin_user: User = Depends(require_admin)
):
    """
    更新用户信息
    - 可更新用户名、邮箱、角色、状态
    - 验证数据唯一性
    - 防护：不能移除最后一个管理员的权限
    """
    # 查询用户
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 更新用户名
    if data.username and data.username != user.username:
        if await User.exists(username=data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        user.username = data.username

    # 更新邮箱
    if data.email and data.email != user.email:
        if await User.exists(email=data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被使用"
            )
        user.email = data.email

    # 更新角色（需要检查是否为最后一个管理员）
    if data.role and data.role != user.role:
        if user.role == "admin" and data.role != "admin":
            # 检查是否为最后一个管理员
            admin_count = await User.filter(role="admin").count()
            if admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "code": "CANNOT_DEMOTE_LAST_ADMIN",
                        "message": "不能移除最后一个管理员的管理员权限"
                    }
                )
        user.role = data.role

    # 更新状态
    if data.is_active is not None:
        user.is_active = data.is_active

    # 保存更新
    await user.save()

    return {
        "success": True,
        "data": UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login,
        ).dict(),
        "message": "用户信息更新成功"
    }


# ============ 重置用户密码 ============

@router.post("/users/{user_id}/reset-password", response_model=dict)
async def reset_user_password(
    user_id: str,
    data: ResetPasswordRequest,
    admin_user: User = Depends(require_admin)
):
    """
    重置用户密码
    - 管理员可以为任何用户重置密码
    - 新密码必须满足强度要求
    """
    # 查询用户
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 更新密码
    user.password_hash = hash_password(data.new_password)
    await user.save()

    return {
        "success": True,
        "message": "密码重置成功",
        "data": {
            "user_id": str(user.id),
            "username": user.username,
            "password_changed_at": user.updated_at,
        }
    }


# ============ 删除用户 ============

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: str,
    cascade: bool = Query(default=True, description="是否级联删除关联数据"),
    admin_user: User = Depends(require_admin)
):
    """
    删除用户
    - 防护：不能删除自己
    - 防护：不能删除最后一个管理员
    - 可选级联删除关联数据（会话、对话）
    """
    # 查询用户
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 防护：不能删除自己
    if str(user.id) == str(admin_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "CANNOT_DELETE_SELF",
                "message": "不能删除自己的账户"
            }
        )

    # 防护：不能删除最后一个管理员
    if user.role == "admin":
        admin_count = await User.filter(role="admin").count()
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "CANNOT_DELETE_LAST_ADMIN",
                    "message": "不能删除最后一个管理员账户"
                }
            )

    # 级联删除关联数据
    deleted_conversations = 0
    deleted_transcripts = 0

    if cascade:
        # 删除用户的所有对话
        conversations = await Conversation.filter(user_id=user_id)
        for conv in conversations:
            # 删除对话的所有 transcript
            transcript_count = await Transcript.filter(conversation_id=conv.id).delete()
            deleted_transcripts += transcript_count
            await conv.delete()
            deleted_conversations += 1

    # 删除用户
    await user.delete()

    return {
        "success": True,
        "message": "用户删除成功",
        "data": {
            "deleted_user_id": str(user_id),
            "deleted_conversations": deleted_conversations,
            "deleted_transcripts": deleted_transcripts,
            "deleted_at": user.updated_at,
        }
    }


# ============ 批量删除用户 ============

@router.post("/users/batch-delete", response_model=dict)
async def batch_delete_users(
    data: BatchDeleteRequest,
    admin_user: User = Depends(require_admin)
):
    """
    批量删除用户
    - 遵循单个删除的所有防护规则
    - 返回每个用户的删除结果
    """
    results = []
    succeeded = 0
    failed = 0

    for user_id in data.user_ids:
        try:
            # 查询用户
            user = await User.get_or_none(id=user_id)
            if not user:
                results.append({
                    "user_id": user_id,
                    "status": "failed",
                    "message": "用户不存在"
                })
                failed += 1
                continue

            # 防护检查
            if str(user.id) == str(admin_user.id):
                results.append({
                    "user_id": user_id,
                    "status": "failed",
                    "message": "不能删除自己"
                })
                failed += 1
                continue

            if user.role == "admin":
                admin_count = await User.filter(role="admin").count()
                if admin_count <= 1:
                    results.append({
                        "user_id": user_id,
                        "status": "failed",
                        "message": "不能删除最后一个管理员"
                    })
                    failed += 1
                    continue

            # 级联删除
            if data.cascade:
                conversations = await Conversation.filter(user_id=user_id)
                for conv in conversations:
                    await Transcript.filter(conversation_id=conv.id).delete()
                    await conv.delete()

            # 删除用户
            await user.delete()

            results.append({
                "user_id": user_id,
                "status": "success",
                "message": "删除成功"
            })
            succeeded += 1

        except Exception as e:
            results.append({
                "user_id": user_id,
                "status": "failed",
                "message": str(e)
            })
            failed += 1

    return {
        "success": True,
        "message": "批量删除完成",
        "data": {
            "total": len(data.user_ids),
            "succeeded": succeeded,
            "failed": failed,
            "results": results
        }
    }
