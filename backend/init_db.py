#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建所有必需的数据库表
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from tortoise import Tortoise
from app.models.user import User
from app.models.conversation import Conversation
from app.models.transcript import Transcript


async def init():
    """初始化数据库连接和表结构"""
    # 数据库配置
    await Tortoise.init(
        db_url='sqlite://./systemx.db',
        modules={'models': [
            'app.models.user',
            'app.models.conversation',
            'app.models.transcript'
        ]}
    )

    # 生成表结构
    await Tortoise.generate_schemas()
    print("✅ 数据库表创建成功！")

    # 验证表是否创建
    conn = Tortoise.get_connection("default")
    tables = await conn.execute_query("SELECT name FROM sqlite_master WHERE type='table';")
    print(f"\n📋 创建的表: {[t[0] for t in tables[1]]}")

    # 关闭连接
    await Tortoise.close_connections()


if __name__ == "__main__":
    print("🚀 开始初始化数据库...")
    asyncio.run(init())
    print("\n✨ 数据库初始化完成！现在可以启动后端服务器了。")
