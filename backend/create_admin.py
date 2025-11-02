#!/usr/bin/env python3
"""创建或更新管理员账户"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.models.user import User
from app.core.security import hash_password
from tortoise import Tortoise

async def create_admin():
    await Tortoise.init(
        db_url='sqlite://./systemx.db',
        modules={'models': ['app.models.user']}
    )

    # 检查rachel用户是否存在
    rachel = await User.get_or_none(username="rachel")
    if rachel:
        # 更新为管理员
        rachel.role = "admin"
        await rachel.save()
        print(f"✅ 用户 'rachel' 已更新为管理员")
        print(f"   用户名: rachel")
        print(f"   邮箱: {rachel.email}")
        print(f"   角色: admin")
    else:
        # 创建新的管理员账户
        admin = await User.create(
            username="admin",
            email="admin@systemx.com",
            password_hash=hash_password("Admin@123"),
            role="admin",
            is_active=True
        )
        print(f"✅ 管理员账户创建成功")
        print(f"   用户名: admin")
        print(f"   密码: Admin@123")
        print(f"   ⚠️  请立即登录并修改密码！")

    await Tortoise.close_connections()

if __name__ == "__main__":
    print("🚀 设置管理员账户...")
    asyncio.run(create_admin())
