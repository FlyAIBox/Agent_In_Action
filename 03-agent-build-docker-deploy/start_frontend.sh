#!/bin/bash

# ============================================================================
# 安装说明（环境配置与依赖安装指南）
# ============================================================================
#
# 1. 创建虚拟环境（推荐）：
#    conda create -n agent101 python=3.10
#    conda activate agent101
#
# 2. 安装依赖：
#    pip install -r requirements.txt
#
# 3. 配置环境变量：
#    创建 .env 文件，添加必要的接口密钥
#    GOOGLE_API_KEY=你的谷歌接口密钥
#
# ============================================================================

echo "🌐 启动AI旅行规划智能体前端"
echo "=============================================="

# 检查conda环境
if ! command -v conda &> /dev/null; then
    echo "❌ Conda 未安装，请先安装Anaconda或Miniconda"
    echo "下载地址: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# 进入前端目录
cd frontend

# 检查是否存在conda虚拟环境
if ! conda env list | grep -q "agent101"; then
    echo "📦 创建conda虚拟环境..."
    conda create -n agent101 python=3.10 -y
fi

# 激活虚拟环境
echo "🔧 激活conda虚拟环境..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate agent101

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 检查后端服务
echo "🔍 检查后端服务状态..."
if ! curl -s http://localhost:8080/health > /dev/null; then
    echo "⚠️  警告: 后端API服务似乎未运行"
    echo "请先启动后端服务: ./start_backend.sh"
    echo "或者在另一个终端中运行: cd backend && python api_server.py"
fi

# 启动Streamlit应用
echo "🚀 启动Streamlit前端应用..."
echo "🌐 前端地址: http://localhost:8501"
echo "=============================================="

streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
