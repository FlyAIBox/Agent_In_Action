![LangChain Academy](https://cdn.prod.website-files.com/65b8cd72835ceeacd4449a53/66e9eba1020525eea7873f96_LCA-big-green%20(2).svg)

# LangChain Academy - 大模型技术学习平台

## 项目介绍

欢迎来到 LangChain Academy！这是一个专为大模型技术初学者设计的综合性学习平台，提供从基础到进阶的完整学习路径。

### 项目特色
- **🎯 面向初学者**：所有教程都配有详细的中文注释和解释
- **📚 循序渐进**：从基础概念到高级应用，逐步深入
- **🛠️ 实践导向**：每个概念都配有可运行的代码示例
- **📖 完整文档**：每个模块都有详细的学习指南和API说明

### 学习模块概览

| 模块 | 主题 | 难度 | 主要内容 |
|------|------|------|----------|
| **Module 0** | 基础环境 | 入门 | Python环境配置、依赖安装、工具准备 |
| **Module 1** | LangGraph入门 | 初级 | 简单图构建、状态管理、条件路由 |
| **Module 2** | 状态管理进阶 | 中级 | 复杂状态模式、状态缩减器、数据库集成 |
| **Module 3** | 调试与监控 | 中级 | 断点调试、时间旅行、人机交互 |
| **Module 4** | 并行与子图 | 高级 | 并行执行、Map-Reduce模式、子图设计 |
| **Module 5** | 内存管理 | 高级 | 内存存储、模式管理、长期记忆 |

### 技术栈
- **核心框架**：LangChain + LangGraph
- **开发语言**：Python 3.11+
- **监控**：LangSmith

### 学习路径建议

#### 🚀 初学者路径
1. **Module 0** → 环境配置
2. **Module 1** → LangGraph基础
3. **Module 2** → 状态管理
4. **Module 3** → 调试技巧

#### 🎯 进阶开发者路径
1. **Module 4** → 高级模式
2. **Module 5** → 内存管理

### 项目结构

每个模块文件夹包含：
- **📓 Jupyter笔记本**：交互式学习教程，配有详细中文注释
- **🎨 Studio目录**：LangGraph Studio配置文件，支持可视化调试
- **📋 依赖文件**：requirements.txt，包含所需依赖包
- **🔧 配置文件**：langgraph.json，图配置和元数据

## 快速开始

### 系统要求

- **Python版本**：3.11+ （推荐3.11或3.12）
- **操作系统**：Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **内存**：至少4GB RAM（推荐8GB+）
- **存储**：至少2GB可用空间

### 一键安装脚本

我们提供了自动安装脚本，可以快速配置完整的学习环境：

#### Windows PowerShell
```powershell
# 下载并运行安装脚本
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/langchain-ai/langchain-academy/main/install.ps1" -OutFile "install.ps1"
.\install.ps1
```

#### macOS/Linux
```bash
# 下载并运行安装脚本
curl -fsSL https://raw.githubusercontent.com/langchain-ai/langchain-academy/main/install.sh | bash
```

### 手动安装

如果你更喜欢手动安装，请按照以下步骤操作：

#### 1. 检查Python版本
```bash
python3 --version
# 确保版本为3.11或更高
```

#### 2. 克隆仓库
```bash
git clone https://github.com/langchain-ai/langchain-academy.git
cd langchain-academy
```

#### 3. 创建虚拟环境
```bash
# 创建虚拟环境
python3 -m venv lc-academy-env

# 激活虚拟环境
# Windows PowerShell
lc-academy-env\Scripts\activate

# macOS/Linux/WSL
source lc-academy-env/bin/activate
```

#### 4. 安装依赖
```bash
# 升级pip到最新版本
python -m pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 如果网络较慢，可以使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 5. 验证安装
```bash
# 启动Jupyter Notebook
jupyter notebook

# 在浏览器中打开 http://localhost:8888
# 导航到 module-1/simple-graph.ipynb 开始学习
```

## 环境配置

### API密钥配置

为了完整运行所有示例，你需要配置以下API密钥：

#### 1. OpenAI API Key（必需）
```bash
# 获取API Key：https://platform.openai.com/api-keys
# Windows PowerShell
$env:OPENAI_API_KEY = "your-openai-api-key-here"

# macOS/Linux/WSL
export OPENAI_API_KEY="your-openai-api-key-here"
```

#### 2. LangSmith配置（推荐）
```bash
# 获取API Key：https://smith.langchain.com/
# Windows PowerShell
$env:LANGSMITH_API_KEY = "your-langsmith-api-key-here"
$env:LANGSMITH_TRACING_V2 = "true"
$env:LANGSMITH_PROJECT = "langchain-academy"

# macOS/Linux/WSL
export LANGSMITH_API_KEY="your-langsmith-api-key-here"
export LANGSMITH_TRACING_V2="true"
export LANGSMITH_PROJECT="langchain-academy"
```

#### 3. Tavily API Key（Module 4需要）
```bash
# 获取API Key：https://tavily.com/
# Windows PowerShell
$env:TAVILY_API_KEY = "your-tavily-api-key-here"

# macOS/Linux/WSL
export TAVILY_API_KEY="your-tavily-api-key-here"
```

### 使用.env文件（推荐）

创建`.env`文件来管理环境变量：

```bash
# 在项目根目录创建.env文件
touch .env

# 编辑.env文件，添加以下内容：
echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env
echo "LANGSMITH_API_KEY=your-langsmith-api-key-here" >> .env
echo "LANGSMITH_TRACING_V2=true" >> .env
echo "LANGSMITH_PROJECT=langchain-academy" >> .env
echo "TAVILY_API_KEY=your-tavily-api-key-here" >> .env
```

## LangGraph Studio 配置

LangGraph Studio 是一个强大的可视化调试工具，让你能够：

- **🎨 图形化界面**：直观地查看和编辑图结构
- **🔍 实时调试**：设置断点，逐步执行
- **📊 状态监控**：实时查看状态变化
- **🔄 交互测试**：直接与图进行交互

### 启动Studio

```bash
# 进入任意模块的studio目录
cd module-1/studio

# 启动LangGraph Studio
langgraph dev

# 你将看到类似输出：
# 🚀 API: http://127.0.0.1:2024
# 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
# 📚 API Docs: http://127.0.0.1:2024/docs
```

### 访问Studio界面

1. 打开浏览器，访问：`https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`
2. 在Studio中，你可以：
   - 查看图的Mermaid可视化
   - 设置断点进行调试
   - 实时查看状态变化
   - 测试不同的输入

### Studio配置

每个模块的`studio`目录都包含：
- `langgraph.json`：图配置文件
- `requirements.txt`：Studio专用依赖
- `.env`：环境变量配置（需要你创建）

## 学习指南

### 开始你的第一个教程

1. **启动Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

2. **打开第一个教程**
   - 导航到 `module-1/simple-graph.ipynb`
   - 这是最简单的LangGraph示例，适合初学者

3. **运行代码**
   - 按 `Shift + Enter` 执行每个代码单元格
   - 观察输出结果和状态变化

### 学习建议

#### 📚 理论学习
- 仔细阅读每个单元格的Markdown说明
- 理解核心概念：状态、节点、边
- 掌握LangGraph的设计哲学

#### 🛠️ 实践练习
- 修改代码参数，观察不同结果
- 尝试添加新的节点和边
- 实验不同的状态模式

#### 🔍 调试技巧
- 使用`print()`语句查看中间状态
- 利用LangGraph Studio进行可视化调试
- 查看执行日志和错误信息

### 常见问题

#### Q: 如何解决依赖安装问题？
A: 确保使用Python 3.11+，并尝试使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### Q: Studio无法启动怎么办？
A: 检查端口2024是否被占用，或尝试指定其他端口：
```bash
langgraph dev --port 2025
```

#### Q: API密钥配置不生效？
A: 确保环境变量正确设置，并重启终端和Jupyter Notebook。

### 获取帮助

- **📖 官方文档**：[LangGraph文档](https://langchain-ai.github.io/langgraph/)
- **💬 社区支持**：[LangChain Discord](https://discord.gg/langchain)
- **🐛 问题反馈**：[GitHub Issues](https://github.com/langchain-ai/langchain-academy/issues)
- **📧 联系我们**：通过GitHub Issues或Discord获取帮助

## 贡献指南

我们欢迎社区贡献！如果你想为这个项目做出贡献：

1. **Fork** 这个仓库
2. **创建** 你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **打开** 一个Pull Request

### 贡献类型
- 🐛 Bug修复
- ✨ 新功能
- 📚 文档改进
- 🎨 代码优化
- 🌍 多语言支持

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 致谢

感谢所有为LangChain生态系统做出贡献的开发者和社区成员！

---

**开始你的LangGraph学习之旅吧！** 🚀
