#!/bin/bash

# ============================================================================
# AI旅行规划智能体 - 环境设置脚本
# ============================================================================
#
# 这个脚本将帮助您快速设置项目环境
#
# 使用方法：
#   chmod +x setup_environment.sh
#   ./setup_environment.sh
#
# ============================================================================

echo "🔧 AI旅行规划智能体 - 环境设置"
echo "=================================================="

# 检查conda是否安装
if ! command -v conda &> /dev/null; then
    echo "❌ Conda 未安装"
    echo ""
    echo "请先安装Anaconda或Miniconda："
    echo "📥 Miniconda下载: https://docs.conda.io/en/latest/miniconda.html"
    echo "📥 Anaconda下载: https://www.anaconda.com/products/distribution"
    echo ""
    echo "安装完成后，请重新运行此脚本"
    exit 1
fi

echo "✅ 检测到Conda环境"

# 检查是否已存在虚拟环境
if conda env list | grep -q "agent101"; then
    echo "⚠️  虚拟环境 'agent101' 已存在"
    read -p "是否要重新创建环境？(y/N): " recreate
    if [[ $recreate =~ ^[Yy]$ ]]; then
        echo "🗑️  删除现有环境..."
        conda env remove -n agent101 -y
    else
        echo "📦 使用现有环境"
    fi
fi

# 创建虚拟环境
if ! conda env list | grep -q "agent101"; then
    echo "📦 创建conda虚拟环境 'agent101'..."
    conda create -n agent101 python=3.10 -y
    
    if [ $? -eq 0 ]; then
        echo "✅ 虚拟环境创建成功"
    else
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
fi

# 激活环境
echo "🔧 激活虚拟环境..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate agent101

# 安装后端依赖
echo "📥 安装后端依赖..."
cd backend
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 后端依赖安装成功"
else
    echo "❌ 后端依赖安装失败"
    exit 1
fi

# 安装前端依赖
echo "📥 安装前端依赖..."
cd ../frontend
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ 前端依赖安装成功"
else
    echo "❌ 前端依赖安装失败"
    exit 1
fi

# 返回后端目录
cd ../backend

# 检查环境变量文件
echo "🔍 检查环境变量配置..."
if [ ! -f ".env" ]; then
    echo "📝 创建.env文件模板..."
    cat > .env << EOF
# OpenAI 兼容 API 配置 (必需)
OPENAI_API_KEY=your_openai_style_api_key_here
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# 和风天气 API (可选)
QWEATHER_API_KEY=your_qweather_api_key_here
QWEATHER_API_BASE=your_api_host

# 模型生成参数
TEMPERATURE=0.7
MAX_TOKENS=4000
TOP_P=0.9
EOF
    echo "✅ .env文件已创建"
    echo "⚠️  请编辑.env文件，配置 OPENAI_API_KEY 及其他可选服务密钥"
else
    echo "✅ .env文件已存在"
fi

# 返回根目录
cd ..

# 创建results目录
if [ ! -d "results" ]; then
    mkdir -p results
    echo "✅ 创建results目录"
fi

echo ""
echo "🎉 环境设置完成！"
echo "=================================================="
echo "1. 启动服务："
echo "   # 终端1 - 启动后端"
echo "   ./start_backend.sh"
echo ""
echo "   # 终端2 - 启动前端"
echo "   ./start_frontend.sh"
echo ""
echo "2. 访问应用："
echo "   🌐 前端界面: http://192.168.172.128:8501"
echo "   📚 API文档: http://192.168.172.128:8000/docs"
echo ""
echo "💡 提示："
echo "   每次使用前请先激活环境: conda activate agent101"
echo ""
echo "=================================================="
