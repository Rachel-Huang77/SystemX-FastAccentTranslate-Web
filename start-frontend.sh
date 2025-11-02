#!/bin/bash
# SystemX Frontend 启动脚本

echo "🚀 启动 SystemX 前端开发服务器..."

# 进入前端目录
cd "$(dirname "$0")/frontend"

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "❌ 依赖未安装，正在安装..."
    npm install
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env 文件不存在，创建默认配置..."
    cat > .env << 'EOF'
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000
EOF
    echo "✅ 已创建 .env 文件"
fi

# 启动服务器
echo "✅ 启动服务器在 http://localhost:5173"
echo ""
npm run dev
