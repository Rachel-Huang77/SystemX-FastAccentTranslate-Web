#!/bin/bash
# SystemX Backend 启动脚本

echo "🚀 启动 SystemX 后端服务器..."

# 进入后端目录
cd "$(dirname "$0")/backend"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行："
    echo "   cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ .env 文件不存在，请先创建："
    echo "   cp .env.example .env"
    echo "   然后编辑 .env 填入 API 密钥"
    exit 1
fi

# 启动服务器
echo "✅ 启动服务器在 http://localhost:8000"
echo "📚 API 文档：http://localhost:8000/docs"
echo "🔍 健康检查：http://localhost:8000/healthz"
echo ""
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
