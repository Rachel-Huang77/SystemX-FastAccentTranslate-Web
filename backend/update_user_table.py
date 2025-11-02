#!/usr/bin/env python3
"""
更新 users 表结构
添加 is_active, updated_at, last_login 字段
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tortoise import Tortoise

async def migrate():
    """执行数据库迁移"""
    await Tortoise.init(
        db_url='sqlite://./systemx.db',
        modules={'models': ['app.models.user']}
    )

    conn = Tortoise.get_connection("default")

    # 检查字段是否存在
    check_columns = await conn.execute_query(
        "PRAGMA table_info(users);"
    )
    existing_columns = [col[1] for col in check_columns[1]]

    print(f"现有字段: {existing_columns}")

    # 添加新字段
    if 'is_active' not in existing_columns:
        await conn.execute_query(
            "ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1;"
        )
        print("✅ 添加 is_active 字段")

    if 'updated_at' not in existing_columns:
        # SQLite doesn't support CURRENT_TIMESTAMP in ALTER TABLE, use NULL and update
        await conn.execute_query(
            "ALTER TABLE users ADD COLUMN updated_at TIMESTAMP NULL;"
        )
        # Update existing rows with current timestamp
        await conn.execute_query(
            "UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL;"
        )
        print("✅ 添加 updated_at 字段")

    if 'last_login' not in existing_columns:
        await conn.execute_query(
            "ALTER TABLE users ADD COLUMN last_login TIMESTAMP NULL;"
        )
        print("✅ 添加 last_login 字段")

    # 为 email 添加唯一索引（如果不存在）
    try:
        await conn.execute_query(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);"
        )
        print("✅ 添加 email 唯一索引")
    except Exception as e:
        print(f"⚠️  email 索引可能已存在: {e}")

    await Tortoise.close_connections()
    print("\n✨ 数据库迁移完成！")

if __name__ == "__main__":
    print("🚀 开始数据库迁移...")
    asyncio.run(migrate())
