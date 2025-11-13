#!/bin/bash

###############################################################################
# AI旅行规划智能体 - 前端启动脚本
# 
# 功能：快速启动优化后的Streamlit前端界面
# 作者：AI Travel Planner Team
# 更新：2025-01-12
###############################################################################

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🌍 AI旅行规划智能体 - 前端启动"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3"
    echo "请先安装Python 3.8或更高版本"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"
echo ""

# 检查Streamlit
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  未检测到Streamlit，正在安装..."
    pip install streamlit
    echo ""
fi

# 检查后端服务
echo "🔍 检查后端服务..."
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ 后端服务运行中"
else
    echo "⚠️  后端服务未运行"
    echo ""
    echo "请先启动后端服务："
    echo "  cd backend && python api_server.py"
    echo ""
    echo "或者使用后台启动："
    echo "  ./start_backend.sh"
    echo ""
    echo "前端界面将继续启动，但功能需要后端支持..."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 启动前端服务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 访问地址:"
echo "   Local:    http://localhost:8501"
echo "   Network:  http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "💡 提示:"
echo "   - 首次加载可能需要几秒钟"
echo "   - 界面已优化为营销展示模式"
echo "   - 适合课程直播和技术演示"
echo ""
echo "🎨 新增功能:"
echo "   ✨ 渐变背景 + 背包客主题"
echo "   ✨ Hero区域和功能特色展示"
echo "   ✨ 世界风光画廊（8个热门目的地）"
echo "   ✨ 专业侧边栏和页脚设计"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 切换到前端目录并启动
cd "$(dirname "$0")/frontend"

# 启动Streamlit
streamlit run streamlit_app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false
