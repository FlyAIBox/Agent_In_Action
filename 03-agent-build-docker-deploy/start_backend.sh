#!/bin/bash

echo "🚀 启动AI旅行规划后端服务"
echo "=================================="

# 杀死可能存在的旧进程
echo "🔧 清理旧进程..."
pkill -f "python api_server.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true

# 等待进程完全停止
sleep 3

# 检查端口是否被占用
if netstat -tlnp 2>/dev/null | grep -q ":8080 "; then
    echo "⚠️  端口8080仍被占用，尝试强制清理..."
    fuser -k 8080/tcp 2>/dev/null || true
    sleep 2
fi

# 进入后端目录
cd backend

# 检查Python环境
echo "🐍 检查Python环境..."
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ FastAPI未安装，正在安装依赖..."
    pip install -r requirements.txt
fi

# 创建日志目录
mkdir -p logs

# 启动服务
echo "🌐 启动后端服务..."
echo "📍 服务地址: http://localhost:8080"
echo "📄 API文档: http://localhost:8080/docs"
echo "🔧 健康检查: http://localhost:8080/health"
echo "📋 日志文件: backend/logs/backend.log"
echo "=================================="

# 启动服务并记录日志
nohup python api_server.py > logs/backend.log 2>&1 &
BACKEND_PID=$!

echo "✅ 后端服务已启动"
echo "📋 进程ID: $BACKEND_PID"

# 等待服务启动
echo "⏳ 等待服务启动..."
for i in {1..30}; do
    if curl -s http://localhost:8080/health >/dev/null 2>&1; then
        echo "✅ 后端服务启动成功！"
        echo "🎯 您现在可以使用前端应用了"
        break
    fi
    echo "等待中... ($i/30)"
    sleep 1
done

# 最终检查
if curl -s http://localhost:8080/health >/dev/null 2>&1; then
    echo ""
    echo "🎉 服务启动完成！"
    echo "📊 服务状态: 正常运行"
    echo "🌐 前端地址: http://localhost:8501"
    echo ""
    echo "💡 使用提示:"
    echo "1. 访问前端页面开始规划旅行"
    echo "2. 如果之前有任务，可以使用手动查询功能"
    echo "3. 查看日志: tail -f -n 200 backend/logs/backend.log"
    echo "4. 停止服务: kill -9 $BACKEND_PID"
else
    echo ""
    echo "❌ 服务启动可能失败"
    echo "🔍 请检查日志: tail -f backend/logs/backend.log"
    echo "🔧 手动启动: cd backend && python api_server.py"
fi

echo ""
echo "=================================="
