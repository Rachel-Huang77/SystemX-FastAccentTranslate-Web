from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional
import re

# ============ 用户列表相关 ============

class UserListQuery(BaseModel):
    """用户列表查询参数"""
    page: int = Field(default=1, ge=1, description="页码")
    limit: int = Field(default=20, ge=1, le=100, description="每页数量")
    search: Optional[str] = Field(default=None, description="搜索关键词")
    role: Optional[str] = Field(default=None, description="角色过滤")
    sort_by: str = Field(default="created_at", description="排序字段")
    sort_order: str = Field(default="desc", description="排序方向")

    @validator("sort_order")
    def validate_sort_order(cls, v):
        if v not in ["asc", "desc"]:
            raise ValueError("排序方向必须是 asc 或 desc")
        return v


class UserResponse(BaseModel):
    """用户响应模式（不包含密码）"""
    id: str
    username: str
    email: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """用户详情响应（包含统计信息）"""
    updated_at: datetime
    statistics: Optional[dict] = None


class UserListResponse(BaseModel):
    """用户列表响应"""
    users: list[UserResponse]
    pagination: dict


# ============ 创建用户相关 ============

class CreateUserRequest(BaseModel):
    """创建用户请求"""
    username: str = Field(..., min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(default="user")

    @validator("username")
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("用户名只能包含字母、数字和下划线")
        return v

    @validator("password")
    def validate_password(cls, v):
        if not re.search(r"[a-z]", v):
            raise ValueError("密码必须包含小写字母")
        if not re.search(r"[A-Z]", v):
            raise ValueError("密码必须包含大写字母")
        if not re.search(r"\d", v):
            raise ValueError("密码必须包含数字")
        return v

    @validator("role")
    def validate_role(cls, v):
        if v not in ["user", "admin"]:
            raise ValueError("角色必须是 user 或 admin")
        return v


# ============ 更新用户相关 ============

class UpdateUserRequest(BaseModel):
    """更新用户请求"""
    username: Optional[str] = Field(None, min_length=3, max_length=32)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @validator("username")
    def validate_username(cls, v):
        if v is not None and not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("用户名只能包含字母、数字和下划线")
        return v

    @validator("role")
    def validate_role(cls, v):
        if v is not None and v not in ["user", "admin"]:
            raise ValueError("角色必须是 user 或 admin")
        return v


# ============ 重置密码相关 ============

class ResetPasswordRequest(BaseModel):
    """重置密码请求"""
    new_password: str = Field(..., min_length=8)

    @validator("new_password")
    def validate_password(cls, v):
        if not re.search(r"[a-z]", v):
            raise ValueError("密码必须包含小写字母")
        if not re.search(r"[A-Z]", v):
            raise ValueError("密码必须包含大写字母")
        if not re.search(r"\d", v):
            raise ValueError("密码必须包含数字")
        return v


# ============ 批量操作相关 ============

class BatchDeleteRequest(BaseModel):
    """批量删除请求"""
    user_ids: list[str] = Field(..., min_items=1)
    cascade: bool = Field(default=True, description="是否级联删除关联数据")
