#!/usr/bin/env python3
"""重置rachel密码为Test123"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.models.user import User
from app.core.security import hash_password
from tortoise import Tortoise

async def reset_password():
    await Tortoise.init(
        db_url='sqlite://./systemx.db',
        modules={'models': ['app.models.user']}
    )

    rachel = await User.get_or_none(username="rachel")
    if rachel:
        rachel.password_hash = hash_password("Test123")
        await rachel.save()
        print(f"✅ rachel密码已重置为: Test123")
    else:
        print("❌ 找不到rachel用户")

    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(reset_password())
