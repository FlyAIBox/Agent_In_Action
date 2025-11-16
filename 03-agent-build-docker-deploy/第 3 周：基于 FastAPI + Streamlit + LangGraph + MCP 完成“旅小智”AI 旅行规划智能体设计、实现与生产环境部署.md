# 第3周：基于 FastAPI + Streamlit + LangGraph + MCP 完成"旅小智"AI 旅行规划智能体设计、实现与生产环境部署

---

## 第一部分：课程导入与项目全景（20分钟）

### 1.1 课程定位与学习目标

**幻灯片1：课程概览**
- **标题**：从 Demo 到生产 - 企业级智能体系统全栈开发
- **核心问题**：
  - ❌ Demo 能跑通，但系统混乱
  - ❌ 本地运行正常，部署就出问题
  - ❌ 环境依赖混乱，无法一键部署
  - ❌ 接口复杂，前后端联调困难
- **解决方案**：
  - ✅ 分层架构设计，建立清晰模块边界
  - ✅ Docker 容器化，实现环境隔离
  - ✅ FastAPI 标准化后端，Streamlit 快速前端
  - ✅ 多智能体协作，提供企业级能力

**幻灯片2：学习路线图**
```
任务 12: 架构设计 (40分钟)
    ↓
任务 13: 全栈开发 (80分钟)
    ├─ Part 1: 后端开发 (FastAPI + LangGraph)
    └─ Part 2: 前端开发 (Streamlit)
    ↓
任务 14: Docker 容器化 (40分钟)
    ↓
生产环境部署
```

**幻灯片3：项目成果展示**
- **最终交付物**：
  1. 🌐 美观的 Web 界面（Streamlit）
  2. 🚀 高性能后端 API（FastAPI）
  3. 🤖 多智能体协作系统（LangGraph）
  4. 🐳 一键部署方案（Docker Compose）
  5. 📚 完整的 API 文档（Swagger UI）

### 7.1 技术栈

**幻灯片：完整技术栈**

```
前端层
├─ Streamlit 1.48.0        # Web 界面框架
└─ requests 2.32.5          # HTTP 客户端

后端层
├─ FastAPI 0.116.1          # API 框架
├─ Uvicorn 0.35.0           # ASGI 服务器
├─ Pydantic 2.11.9          # 数据验证
└─ python-multipart 0.0.20  # 文件上传

智能体层
├─ LangGraph 0.6.7          # 工作流编排
├─ LangChain 0.3.27         # LLM 集成
├─ langchain-openai 0.3.31  # OpenAI 适配
└─ langchain-community      # 社区工具

工具层
├─ DuckDuckGo Search 8.1.1  # 搜索引擎
├─ MCP 1.17.0               # 模型上下文协议
└─ beautifulsoup4 4.13.4    # HTML 解析

配置层
├─ python-dotenv 1.1.1      # 环境变量
└─ psutil 5.9.0             # 系统监控

测试层
├─ pytest 8.4.1             # 测试框架
└─ pytest-asyncio 1.1.0     # 异步测试

部署层
├─ Docker                   # 容器化
└─ Docker Compose           # 多容器编排
```

### 7.2 架构设计亮点

**幻灯片：核心设计亮点**

| 亮点               | 实现方式                      | 价值             |
| ------------------ | ----------------------------- | ---------------- |
| 🎯 **分层架构**     | 前端/后端/智能体/工具四层分离 | 职责清晰，易维护 |
| 🤖 **多智能体协作** | LangGraph 状态机编排          | 灵活可扩展       |
| ⚡ **异步处理**     | FastAPI + asyncio             | 高并发性能       |
| 🔧 **工具系统**     | LangChain @tool 装饰器        | 统一工具接口     |
| 🔐 **配置管理**     | .env + Pydantic 验证          | 安全且类型安全   |
| 📊 **状态管理**     | JSON 持久化 + 内存缓存        | 可恢复可追踪     |
| 🐳 **容器化**       | Docker + Compose              | 一键部署         |
| 💬 **自然语言交互** | LLM 意图识别                  | 用户体验好       |

### 7.3 学到的核心能力

**幻灯片：技能树**

```
1. 架构设计能力
   ├─ 分层架构设计
   ├─ 模块边界划分
   ├─ 接口设计规范
   └─ 数据模型设计

2. 后端开发能力
   ├─ FastAPI 开发
   ├─ 异步编程
   ├─ API 设计
   ├─ 数据验证
   └─ 错误处理

3. 智能体开发能力
   ├─ LangGraph 编排
   ├─ 多智能体协作
   ├─ 状态管理
   ├─ 工具集成
   └─ 提示词工程

4. 前端开发能力
   ├─ Streamlit 开发
   ├─ 交互设计
   ├─ 状态管理
   └─ API 集成

5. 运维部署能力
   ├─ Docker 容器化
   ├─ Docker Compose 编排
   ├─ 日志管理
   ├─ 监控告警
   └─ 故障排除
```

---

## 第二部分：任务 12 - 架构设计（40分钟）

### 2.1 系统架构设计原则

**幻灯片4：企业级架构设计思路**
- **为什么需要架构设计？**
  - 单文件脚本 → 可维护的系统
  - 硬编码配置 → 环境隔离
  - 同步阻塞 → 异步高并发
  - 本地运行 → 生产部署

**幻灯片5：分层架构设计**
```
┌─────────────────────────────────────────────┐
│         前端层 (Streamlit)                   │
│  - 用户界面                                   │
│  - 交互组件                                   │
│  - 状态管理                                   │
└─────────────────────────────────────────────┘
                    ↕ HTTP/REST API
┌─────────────────────────────────────────────┐
│         后端层 (FastAPI)                     │
│  - API 路由                                   │
│  - 请求处理                                   │
│  - 异步任务                                   │
│  - 状态持久化                                 │
└─────────────────────────────────────────────┘
                    ↕ Python 调用
┌─────────────────────────────────────────────┐
│       智能体层 (LangGraph)                   │
│  - 协调员智能体                               │
│  - 专业智能体（旅行顾问、预算优化师等）        │
│  - 状态管理                                   │
│  - 工作流编排                                 │
└─────────────────────────────────────────────┘
                    ↕ 工具调用
┌─────────────────────────────────────────────┐
│         工具层 (Tools)                       │
│  - DuckDuckGo 搜索                           │
│  - 天气查询 (MCP)                            │
└─────────────────────────────────────────────┘
```

### 2.2 模块边界与职责划分

**幻灯片6：模块职责矩阵**
| 层级       | 模块                  | 职责               | 技术栈               |
| ---------- | --------------------- | ------------------ | -------------------- |
| **前端**   | `streamlit_app.py`    | 用户交互、结果展示 | Streamlit            |
| **后端**   | `api_server.py`       | API 服务、任务调度 | FastAPI, Uvicorn     |
| **智能体** | `langgraph_agents.py` | 多智能体协作       | LangGraph, LangChain |
| **工具**   | `travel_tools.py`     | 外部服务集成       | DuckDuckGo, MCP      |
| **配置**   | `config/`             | 配置管理           | python-dotenv        |
| **数据**   | `models/`             | 数据模型           | Pydantic             |

**幻灯片7：API 接口设计规范（RESTful）**
```python
# 核心接口设计
GET  /              # 系统信息
GET  /health        # 健康检查
POST /plan          # 创建规划任务
GET  /status/{id}   # 查询任务状态
GET  /download/{id} # 下载结果
POST /chat          # 自然语言交互
```

**幻灯片8：数据模型设计**
```python
# 请求模型
class TravelRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget_range: str
    group_size: int
    interests: List[str]
    # ... 更多字段

# 响应模型
class PlanningStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    current_agent: str
    message: str
    result: Optional[Dict]
```

### 2.3 配置管理与环境隔离

**幻灯片9：配置管理策略**
```bash
# 环境变量管理（.env）
OPENAI_API_KEY=sk-xxx              # 必需
OPENAI_BASE_URL=https://...        # 可选
OPENAI_MODEL=deepseek-chat         # 可选

# 可选服务
QWEATHER_API_KEY=xxx               # 天气服务
```

**幻灯片10：配置类设计**
```python
# config/langgraph_config.py
class LangGraphConfig:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "deepseek-chat")
        # ...
    
    def validate_config(self):
        """配置验证"""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY 未配置")
```

---

## 第三部分：任务 13 Part 1 - 后端开发（40分钟）

### 3.1 FastAPI 框架基础

**幻灯片11：为什么选择 FastAPI？**
- ⚡ **高性能**：基于 Starlette 和 Pydantic，性能媲美 NodeJS 和 Go
- 🚀 **快速开发**：自动生成 API 文档（Swagger UI）
- 🔒 **类型安全**：基于 Python 类型提示，IDE 友好
- 🔄 **异步支持**：原生支持 async/await
- 📝 **数据验证**：自动验证请求和响应数据

**幻灯片12：FastAPI 核心特性演示**
```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI(
    title="旅小智 API",
    description="AI旅行规划智能体",
    version="2.0.0"
)

# 1. 数据验证
class TravelRequest(BaseModel):
    destination: str
    start_date: str
    group_size: int

# 2. 异步路由
@app.post("/plan")
async def create_plan(request: TravelRequest):
    return {"task_id": "xxx", "status": "started"}

# 3. 后台任务
@app.post("/plan")
async def create_plan(
    request: TravelRequest, 
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(run_planning, request)
    return {"task_id": "xxx"}
```

### 3.2 API 路由设计与实现

**幻灯片13：核心 API 路由实现**
```python
# 1. 健康检查端点
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "llm_model": config.OPENAI_MODEL,
        "api_key_configured": bool(config.OPENAI_API_KEY),
        "active_tasks": len(planning_tasks)
    }

# 2. 创建规划任务
@app.post("/plan", response_model=PlanningResponse)
async def create_travel_plan(
    request: TravelRequest, 
    background_tasks: BackgroundTasks
):
    task_id = str(uuid.uuid4())
    # 初始化任务状态
    planning_tasks[task_id] = {
        "status": "started",
        "progress": 0,
        "request": request.model_dump()
    }
    # 添加后台任务
    background_tasks.add_task(run_planning_task, task_id, request)
    return PlanningResponse(task_id=task_id, status="started")
```

**幻灯片14：异步任务处理**
```python
async def run_planning_task(task_id: str, travel_request: Dict):
    try:
        # 1. 更新任务状态
        planning_tasks[task_id]["status"] = "processing"
        planning_tasks[task_id]["progress"] = 30
        
        # 2. 调用 LangGraph 智能体
        travel_agents = LangGraphTravelAgents()
        result = await asyncio.wait_for(
            run_langgraph(), 
            timeout=300.0
        )
        
        # 3. 保存结果
        if result["success"]:
            planning_tasks[task_id]["status"] = "completed"
            planning_tasks[task_id]["result"] = result
            await save_planning_result(task_id, result)
    except asyncio.TimeoutError:
        # 超时处理
        planning_tasks[task_id]["status"] = "timeout"
    except Exception as e:
        # 错误处理
        planning_tasks[task_id]["status"] = "failed"
```

### 3.3 LangGraph 智能体集成

**幻灯片15：LangGraph 多智能体架构**
```
┌─────────────────────────────────────────┐
│        协调员智能体 (Coordinator)        │
│   - 分析请求                             │
│   - 路由决策                             │
│   - 结果整合                             │
└─────────────────────────────────────────┘
           │
           ├──→ 旅行顾问 (Travel Advisor)
           ├──→ 天气分析师 (Weather Analyst)
           ├──→ 预算优化师 (Budget Optimizer)
           ├──→ 当地专家 (Local Expert)
           └──→ 行程规划师 (Itinerary Planner)
```

**幻灯片16：状态管理设计**
```python
class TravelPlanState(TypedDict):
    """旅行规划状态"""
    messages: List[BaseMessage]        # 对话历史
    destination: str                   # 目的地
    duration: int                      # 天数
    budget_range: str                  # 预算范围
    interests: List[str]               # 兴趣
    group_size: int                    # 人数
    travel_dates: str                  # 日期
    current_agent: str                 # 当前智能体
    agent_outputs: Dict[str, Any]      # 智能体输出
    final_plan: Dict[str, Any]         # 最终计划
    iteration_count: int               # 迭代次数
```

**幻灯片17：智能体节点实现**
```python
def travel_advisor_node(state: TravelPlanState) -> TravelPlanState:
    """旅行顾问节点"""
    # 1. 获取当前状态
    destination = state["destination"]
    interests = state["interests"]
    
    # 2. 构造提示词
    prompt = f"""你是专业的旅行顾问...
    目的地: {destination}
    兴趣: {', '.join(interests)}
    """
    
    # 3. 调用 LLM
    messages = [SystemMessage(content=prompt)]
    response = llm.invoke(messages)
    
    # 4. 更新状态
    state["agent_outputs"]["travel_advisor"] = {
        "response": response.content,
        "status": "completed"
    }
    return state
```

### 3.4 工具调用层实现

**幻灯片18：DuckDuckGo 搜索工具**
```python
from langchain_core.tools import tool

@tool
def search_destination_info(destination: str) -> str:
    """搜索目的地信息"""
    try:
        results = DDGS().text(
            f"{destination} 旅游攻略 景点推荐",
            region="cn-zh",
            safesearch="moderate",
            max_results=3
        )
        return format_results(results)
    except Exception as e:
        return f"搜索失败: {str(e)}"

@tool
def search_weather_info(destination: str, date: str) -> str:
    """搜索天气信息"""
    # 实现逻辑...

# 工具列表
ALL_TOOLS = [
    search_destination_info,
    search_weather_info,
    search_attractions,
    # ...
]
```

**幻灯片19：MCP 天气服务器集成**
```python
# tools/weather_server_mcp.py
from mcp.server import Server
from mcp.types import Tool

async def serve():
    server = Server("weather-server")
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        return [
            Tool(
                name="get_weather",
                description="获取城市天气",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"}
                    }
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "get_weather":
            return await get_weather(arguments["city"])
```

---

## 第四部分：任务 13 Part 2 - 前端开发（40分钟）

### 4.1 Streamlit 框架基础

**幻灯片20：为什么选择 Streamlit？**
- 🚀 **快速开发**：纯 Python，无需 HTML/CSS/JS
- 🎨 **美观界面**：内置现代化 UI 组件
- 🔄 **实时交互**：自动重新运行，实时更新
- 📊 **数据可视化**：集成 Plotly、Matplotlib
- 🎯 **专注业务**：专注数据和逻辑，不用操心前端细节

**幻灯片21：Streamlit 核心组件**
```python
import streamlit as st

# 1. 页面配置
st.set_page_config(
    page_title="旅小智",
    page_icon="🤖",
    layout="wide"
)

# 2. 布局组件
col1, col2 = st.columns(2)
with col1:
    st.text_input("目的地")
with col2:
    st.date_input("出发日期")

# 3. 交互组件
if st.button("开始规划"):
    with st.spinner("规划中..."):
        result = call_api()
    st.success("规划完成！")

# 4. 状态管理
if "task_id" not in st.session_state:
    st.session_state.task_id = None
```

### 4.2 用户输入界面设计

**幻灯片22：表单设计最佳实践**
```python
def create_travel_form():
    """创建旅行规划表单"""
    with st.form("travel_form"):
        # 基本信息
        destination = st.text_input(
            "目的地",
            placeholder="例如: 北京, 上海, 成都"
        )
        
        # 日期选择
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("出发日期")
        with col2:
            end_date = st.date_input("返回日期")
        
        # 兴趣爱好（多选）
        interests = st.multiselect(
            "兴趣爱好",
            ["历史", "美食", "自然风光", "购物"]
        )
        
        # 提交按钮
        submitted = st.form_submit_button("开始规划")
        
        if submitted:
            # 验证输入
            if not destination:
                st.error("请输入目的地")
                return None
            return build_request(destination, start_date, ...)
```

### 4.3 实时进度监控

**幻灯片23：进度条与状态更新**
```python
def display_planning_progress(task_id: str):
    """显示规划进度"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    max_attempts = 60
    for attempt in range(max_attempts):
        # 查询任务状态
        status = get_planning_status(task_id)
        
        if status:
            progress = status.get("progress", 0)
            message = status.get("message", "处理中...")
            
            # 更新UI
            progress_bar.progress(progress / 100)
            status_text.info(f"🤖 {message}")
            
            # 检查是否完成
            if status["status"] == "completed":
                st.success("规划完成！")
                return status["result"]
            elif status["status"] == "failed":
                st.error("规划失败")
                return None
        
        time.sleep(1)
```

### 4.4 结果可视化展示

**幻灯片24：智能体输出展示**
```python
def display_planning_result(result: Dict):
    """显示规划结果"""
    st.markdown("### 📋 规划概览")
    
    # 基本信息指标
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("目的地", result["destination"])
    with col2:
        st.metric("天数", f"{result['duration']}天")
    with col3:
        st.metric("预算", result["budget_range"])
    
    # 智能体建议
    st.markdown("### 🤖 AI智能体建议")
    for agent_name, output in result["agent_outputs"].items():
        with st.expander(f"{agent_name} 建议"):
            st.text_area(
                "建议内容",
                value=output["response"],
                height=200
            )
```

### 4.5 自然语言交互界面

**幻灯片25：聊天式交互**
```python
def display_chat_interface():
    """显示自然语言交互界面"""
    st.markdown("## 💬 告诉旅小智你的旅行想法")
    
    # 输入框
    user_input = st.text_area(
        "描述您的旅行需求",
        placeholder="例如：我想下周去北京玩3天...",
        height=150
    )
    
    # 快捷示例
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("北京3日游"):
            user_input = "北京3日游，历史文化"
    
    if user_input:
        # 调用后端 /chat 接口
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"message": user_input}
        )
        
        chat_response = response.json()
        st.info(chat_response["clarification"])
        
        # 如果可以创建任务
        if chat_response["can_proceed"]:
            task_id = chat_response["task_id"]
            st.success(f"任务已创建: {task_id}")
```

---

## 第五部分：任务 14 - Docker 容器化（40分钟）

### 5.1 Docker 基础与最佳实践

**幻灯片26：为什么需要容器化？**
| 痛点               | 容器化解决方案        |
| ------------------ | --------------------- |
| 🔴 "在我电脑上能跑" | ✅ 环境一致性保证      |
| 🔴 依赖安装困难     | ✅ 镜像包含所有依赖    |
| 🔴 多服务协调复杂   | ✅ Docker Compose 编排 |
| 🔴 部署流程繁琐     | ✅ 一键启动/停止       |
| 🔴 扩展困难         | ✅ 容器化天然支持扩展  |

**幻灯片27：Dockerfile 最佳实践**
```dockerfile
# 1. 选择合适的基础镜像
FROM python:3.10-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 安装系统依赖（如需要）
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. 先复制依赖文件（利用缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 再复制应用代码
COPY . .

# 6. 创建必要的目录
RUN mkdir -p results logs

# 7. 暴露端口
EXPOSE 8080

# 8. 健康检查
HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:8080/health || exit 1

# 9. 启动命令
CMD ["python", "api_server.py"]
```

### 5.2 后端服务容器化

**幻灯片28：后端 Dockerfile 解析**
```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录
RUN mkdir -p results logs

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "api_server.py"]
```

**关键点说明**：
1. **分层构建**：依赖安装和代码复制分开，充分利用 Docker 缓存
2. **清理冗余**：删除 apt 缓存减小镜像体积
3. **健康检查**：自动监控容器健康状态
4. **端口暴露**：明确服务监听端口

### 5.3 前端服务容器化

**幻灯片29：前端 Dockerfile 解析**
```dockerfile
# frontend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]
```

**Streamlit 特殊配置**：
- `--server.address=0.0.0.0`：允许外部访问
- `--server.headless=true`：无头模式运行
- `--browser.gatherUsageStats=false`：禁用数据收集

### 5.4 Docker Compose 多容器编排

**幻灯片30：docker-compose.yml 解析**
```yaml
version: '3.8'

services:
  # 后端服务
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    env_file:
      - ./backend/.env
    volumes:
      - ./results:/app/results
    networks:
      - travel-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 前端服务
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    environment:
      - API_BASE_URL=http://backend:8080
    depends_on:
      - backend
    networks:
      - travel-network
    restart: unless-stopped

networks:
  travel-network:
    driver: bridge

volumes:
  results:
    driver: local
```

**幻灯片31：Docker Compose 关键配置**
| 配置项        | 作用     | 说明                 |
| ------------- | -------- | -------------------- |
| `build`       | 镜像构建 | 指定 Dockerfile 位置 |
| `ports`       | 端口映射 | 主机端口:容器端口    |
| `env_file`    | 环境变量 | 从文件注入配置       |
| `volumes`     | 数据卷   | 持久化数据           |
| `networks`    | 网络配置 | 服务间通信           |
| `depends_on`  | 依赖关系 | 启动顺序控制         |
| `restart`     | 重启策略 | 异常自动重启         |
| `healthcheck` | 健康检查 | 服务状态监控         |

### 5.5 容器网络与数据卷

**幻灯片32：容器间通信**
```yaml
# 前端容器访问后端
environment:
  # ❌ 错误：使用 localhost
  - API_BASE_URL=http://localhost:8080
  
  # ✅ 正确：使用服务名
  - API_BASE_URL=http://backend:8080
```

**Docker Compose 网络特性**：
- 自动 DNS 解析：服务名 = 主机名
- 网络隔离：同一网络内服务可互访
- 端口无需暴露：内部通信使用容器端口

**幻灯片33：数据持久化**
```yaml
volumes:
  # 绑定挂载（开发环境）
  - ./results:/app/results
  
  # 命名卷（生产环境）
  - results_data:/app/results

volumes:
  results_data:
    driver: local
```

### 5.6 一键部署与运维

**幻灯片34：Docker Compose 命令**
```bash
# 构建并启动所有服务
docker compose up --build

# 后台运行
docker compose up -d --build

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f backend
docker compose logs -f frontend

# 停止服务
docker compose down

# 停止并删除卷
docker compose down -v

# 重启服务
docker compose restart backend
```

**幻灯片35：启动脚本自动化**
```bash
#!/bin/bash
# start_all.sh

echo "🚀 启动旅小智服务..."

# 1. 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装"
    exit 1
fi

# 2. 检查环境变量
if [ ! -f "backend/.env" ]; then
    echo "❌ 请先配置 backend/.env"
    exit 1
fi

# 3. 构建并启动
docker compose up --build -d

# 4. 等待服务就绪
echo "⏳ 等待服务启动..."
sleep 10

# 5. 健康检查
if curl -f http://localhost:8080/health; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端服务异常"
fi

if curl -f http://localhost:8501/_stcore/health; then
    echo "✅ 前端服务正常"
else
    echo "❌ 前端服务异常"
fi

echo "🎉 服务启动完成！"
echo "前端: http://localhost:8501"
echo "后端: http://localhost:8080/docs"
```

---

## 第六部分：生产环境部署与运维（30分钟）

### 6.1 环境变量与密钥管理

**幻灯片36：生产环境配置管理**
```bash
# 开发环境
backend/.env              # Git ignore
frontend/.env             # Git ignore

# 生产环境（推荐方案）
1. 环境变量注入
   docker run -e OPENAI_API_KEY=xxx ...

2. Docker secrets（Swarm模式）
   echo "sk-xxx" | docker secret create openai_key -

3. Kubernetes ConfigMap/Secret
   kubectl create secret generic api-keys \
     --from-literal=openai-key=sk-xxx

4. 云平台密钥管理
   - AWS Secrets Manager
   - Azure Key Vault
   - Google Secret Manager
```

**幻灯片37：安全最佳实践**
| 安全措施     | 说明                   |
| ------------ | ---------------------- |
| 🔐 密钥加密   | 使用云平台密钥管理服务 |
| 🚫 禁止硬编码 | 代码中不出现密钥       |
| 🔒 最小权限   | API 密钥只分配必要权限 |
| 🔄 定期轮换   | 定期更换密钥           |
| 📝 审计日志   | 记录密钥使用情况       |
| 🛡️ 网络隔离   | 限制服务间访问         |

### 6.2 日志管理与监控

**幻灯片38：日志配置**
```python
# 后端日志配置
import logging

def setup_logger():
    logger = logging.getLogger('api_server')
    logger.setLevel(logging.INFO)
    
    # 文件处理器
    fh = logging.FileHandler('logs/backend.log')
    fh.setLevel(logging.INFO)
    
    # 格式化
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    
    logger.addHandler(fh)
    return logger

# 使用日志
logger.info(f"任务 {task_id} 开始执行")
logger.error(f"任务 {task_id} 执行失败: {error}")
```

**幻灯片39：Docker 日志管理**
```bash
# 查看实时日志
docker compose logs -f

# 查看最近100行
docker compose logs --tail=100

# 查看特定服务
docker compose logs -f backend

# 日志驱动配置（docker-compose.yml）
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 6.3 健康检查与故障恢复

**幻灯片40：健康检查实现**
```python
# API 健康检查端点
@app.get("/health")
async def health_check():
    try:
        # 1. 检查配置
        if not config.OPENAI_API_KEY:
            return {
                "status": "warning",
                "message": "API密钥未配置"
            }
        
        # 2. 检查系统资源
        import psutil
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        
        # 3. 返回状态
        return {
            "status": "healthy",
            "llm_model": config.OPENAI_MODEL,
            "system": {
                "cpu_usage": f"{cpu}%",
                "memory_usage": f"{memory.percent}%"
            },
            "active_tasks": len(planning_tasks)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

**幻灯片41：Docker 健康检查配置**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s      # 每30秒检查一次
  timeout: 10s       # 超时时间10秒
  retries: 3         # 失败3次标记为不健康
  start_period: 40s  # 启动宽限期40秒
```

### 6.4 性能优化策略

**幻灯片42：后端性能优化**
```python
# 1. 异步优化
async def run_planning_task(task_id: str, request: Dict):
    # 使用线程池避免阻塞
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(heavy_task)
        result = await asyncio.wrap_future(future)

# 2. 超时控制
try:
    result = await asyncio.wait_for(
        run_langgraph(), 
        timeout=300.0
    )
except asyncio.TimeoutError:
    # 降级处理
    result = get_simplified_plan()

# 3. 任务状态持久化
def save_tasks_state():
    """定期保存任务状态"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(planning_tasks, f)
```

**幻灯片43：前端性能优化**
```python
# 1. Session State 管理
if "task_id" not in st.session_state:
    st.session_state.task_id = None

# 2. 缓存配置
@st.cache_data(ttl=3600)
def load_destinations():
    return fetch_destinations()

# 3. 减少重新运行
if st.button("提交"):
    st.session_state.submitted = True
    st.rerun()

# 4. 异步轮询优化
time.sleep(5)  # 降低轮询频率
```

### 6.5 故障排除清单

**幻灯片44：常见问题诊断**
| 症状               | 可能原因      | 解决方案                   |
| ------------------ | ------------- | -------------------------- |
| 🔴 后端启动失败     | API密钥未配置 | 检查 `.env` 文件           |
| 🔴 前端无法连接后端 | 网络配置错误  | 使用服务名而非 localhost   |
| 🔴 任务超时         | LLM响应慢     | 增加超时时间，添加降级方案 |
| 🔴 容器无法启动     | 端口被占用    | 检查端口占用，修改映射     |
| 🔴 依赖安装失败     | 网络问题      | 使用国内镜像源             |
| 🔴 内存溢出         | 任务堆积      | 限制并发任务数             |

**幻灯片45：排查命令速查**
```bash
# 1. 检查容器状态
docker compose ps

# 2. 查看容器日志
docker compose logs backend
docker compose logs frontend

# 3. 进入容器调试
docker compose exec backend bash

# 4. 检查网络
docker network ls
docker network inspect travel-network

# 5. 检查端口
netstat -tlnp | grep 8080

# 6. 测试API
curl http://localhost:8080/health
curl http://localhost:8080/docs

# 7. 重启服务
docker compose restart backend
```

