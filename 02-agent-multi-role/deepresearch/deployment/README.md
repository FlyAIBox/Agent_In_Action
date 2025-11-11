# 深度研究助手 - 容器化部署指南

本文档介绍如何使用 LangGraph Platform 部署深度研究助手（Deep Research Assistant）系统。

## 系统概述

深度研究助手是一个基于 LangGraph 的**多智能体协作研究系统**，能够针对任意主题自动生成全面、多角度的研究报告。

### 核心功能

1. **多视角分析**
   - 根据研究主题自动生成 3-5 个不同视角的 AI 分析师
   - 每个分析师代表特定的专业领域或关注点
   - 支持人类审核和调整分析师配置（通过中断点实现）

2. **深度信息收集**
   - 每个分析师通过"访谈"方式进行深度研究
   - 自动生成针对性问题，并通过搜索获取答案
   - 支持 Web 搜索（Tavily）和百科检索（Wikipedia）
   - 多轮对话确保信息的深度和完整性

3. **结构化报告生成**
   - 自动整合所有分析师的研究成果
   - 生成包含引言、主体、结论和来源引用的完整报告
   - 使用 Markdown 格式，结构清晰，便于阅读

4. **工作流架构**
   - 使用 Map-Reduce 模式实现并行处理
   - 支持人机协同（Human-in-the-loop）
   - 基于 LangGraph Checkpointer 的状态持久化机制

## 系统架构

```
主工作流 (Map-Reduce 模式)
┌────────────────────────────────────────────────────────────────┐
│                      深度研究助手系统                           │
├────────────────────────────────────────────────────────────────┤
│ 1. 生成分析师 → 2. 人机协同中断 → 3. 并行访谈 → 4. 整合报告   │
│                                        ↓                        │
│                    Map 阶段（并行执行）                         │
│    ┌──────────────┬──────────────┬──────────────┐             │
│    │ 分析师 1     │ 分析师 2     │ 分析师 N     │             │
│    │ ↓            │ ↓            │ ↓            │             │
│    │ 访谈子图     │ 访谈子图     │ 访谈子图     │             │
│    │ ↓            │ ↓            │ ↓            │             │
│    │ 报告小节 1   │ 报告小节 2   │ 报告小节 N   │             │
│    └──────────────┴──────────────┴──────────────┘             │
│                          ↓                                     │
│                  Reduce 阶段（整合）                           │
│         ┌────────────┬──────────┬──────────┐                  │
│         │ 写主体     │ 写引言   │ 写结论   │                  │
│         └────────────┴──────────┴──────────┘                  │
│                          ↓                                     │
│                    最终报告组装                                │
└────────────────────────────────────────────────────────────────┘
         ↓                ↓                ↓           ↓
    ┌────────┐      ┌────────┐      ┌────────┐  ┌──────────┐
    │OpenAI  │      │Memory  │      │Tavily  │  │Wikipedia │
    │GPT-4o  │      │Saver   │      │Search  │  │ Loader   │
    └────────┘      └────────┘      └────────┘  └──────────┘
      (LLM)      (Checkpointer)    (Web搜索)    (百科检索)
```

## 技术栈

- **LangGraph**: 智能体工作流编排框架
- **LangChain**: LLM 应用集成框架
- **OpenAI GPT-4o**: 大语言模型（推理引擎）
- **Tavily Search**: 实时 Web 搜索 API
- **Wikipedia**: 权威知识库检索
- **PostgreSQL**: 状态持久化数据库（LangGraph Checkpointer）
- **Redis**: 消息队列和缓存

## 快速开始

### 前置要求

- Docker 和 Docker Compose
- LangGraph CLI (`pip install langgraph-cli`)
- OpenAI API 密钥
- Tavily API 密钥（可选）
- LangSmith API 密钥（可选，用于追踪）

### 1. 环境配置

复制环境变量示例文件并配置：

```bash
cp .env-example .env
```

编辑 `.env` 文件，填入你的 API 密钥：

```bash
# OpenAI API 配置
OPENAI_BASE_URL="https://api.openai.com/v1"
OPENAI_API_KEY="sk-your-openai-api-key"

# Tavily 搜索 API（可选）
TAVILY_API_KEY="tvly-your-tavily-api-key"

# LangSmith 追踪（可选）
LANGSMITH_API_KEY="lsv2-your-langsmith-api-key"
```

### 2. 构建 Docker 镜像

使用 LangGraph CLI 构建镜像：

```bash
# 进入部署目录
cd 02-agent-multi-role/deepresearch/deployment

# 构建镜像
langgraph build -t research-assistant-image
```

构建过程说明：
- 基于 `langgraph.json` 配置创建镜像
- 安装 Python 3.11 和所有依赖
- 配置 LangGraph Server

### 3. 启动服务

使用 Docker Compose 启动所有服务：

```bash
docker compose --env-file .env up -d
```

这将启动三个容器：
- **langgraph-redis**: Redis 消息队列（端口 6380）
- **langgraph-postgres**: PostgreSQL 数据库（端口 5433）
- **langgraph-api**: LangGraph Server（端口 8124）

### 4. 验证部署

访问以下端点验证部署：

- **API 根路径**: http://localhost:8124
- **API 文档**: http://localhost:8124/docs
- **健康检查**: http://localhost:8124/health

### 5. 使用 LangGraph Studio

在 LangGraph Studio 中连接到部署：

```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8124
```

## 使用指南

### 基本使用流程

1. **创建线程**：每个研究任务使用独立的线程
2. **启动研究**：提供研究主题和分析师数量
3. **人工审核**：在生成分析师后可以进行调整
4. **执行访谈**：系统自动并行执行多个访谈
5. **生成报告**：获取最终的研究报告

### Python SDK 示例

```python
from langgraph_sdk import get_client

# 连接到部署的 LangGraph Server
client = get_client(url="http://localhost:8124")

# 创建线程（每个研究任务使用独立线程）
thread = await client.threads.create()

# 准备输入数据
input_data = {
    "topic": "人工智能在医疗领域的应用",
    "max_analysts": 3
}

# 执行研究流程（流式输出）
async for chunk in client.runs.stream(
    thread["thread_id"],
    "research_assistant",
    input=input_data,
    stream_mode="values"
):
    # 处理流式输出
    if "final_report" in chunk:
        print(chunk["final_report"])
        
# 或者使用非流式方式
result = await client.runs.create_blocking(
    thread["thread_id"],
    "research_assistant",
    input=input_data
)
print(result["final_report"])
```

### Remote Graph 示例

```python
from langgraph.pregel.remote import RemoteGraph

# 连接到远程部署的图
remote_graph = RemoteGraph("research_assistant", url="http://localhost:8124")

# 准备输入数据
input_data = {
    "topic": "区块链技术的发展趋势",
    "max_analysts": 3
}

# 执行研究（异步）
result = await remote_graph.ainvoke(input_data)

# 获取最终报告
print(result["final_report"])

# 或者使用流式输出
async for chunk in remote_graph.astream(input_data, stream_mode="values"):
    if "final_report" in chunk:
        print(chunk["final_report"])
```

## 配置说明

### 配置文件

#### langgraph.json

定义图的配置和依赖：

```json
{
    "graphs": {
      "research_assistant": "./research_assistant.py:graph"
    },
    "python_version": "3.11",
    "dependencies": ["."]
}
```

此文件告诉 LangGraph CLI：
- 图的入口点：`research_assistant.py` 文件中的 `graph` 对象
- Python 版本：3.11
- 依赖安装：当前目录（会读取 `pyproject.toml` 或 `requirements.txt`）

#### 研究参数配置

研究参数通过 **输入数据** 传递，而不是通过配置文件：

```python
# 通过输入数据控制研究行为
input_data = {
    "topic": "研究主题",           # 必需：研究的具体主题
    "max_analysts": 3,             # 可选：生成的分析师数量（默认3）
    "human_analyst_feedback": ""   # 可选：人类对分析师的反馈
}
```

**重要说明**：
- `max_interview_turns` 在代码中硬编码为 2（参见 `route_messages` 函数）
- `enable_human_feedback` 功能始终启用（`interrupt_before=['human_feedback']` 硬编码）
- 如需调整这些参数，需要修改 `research_assistant.py` 源代码

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | 是 |
| `OPENAI_BASE_URL` | OpenAI API 地址 | 否 |
| `TAVILY_API_KEY` | Tavily 搜索 API 密钥 | 否 |
| `LANGSMITH_API_KEY` | LangSmith 追踪密钥 | 否 |

## 测试

运行测试脚本验证部署：

```bash
python test_connection.py
```

测试内容包括：
- 连接验证
- 分析师生成测试
- 访谈流程测试
- 报告生成测试

## 故障排查

### 常见问题

1. **端口冲突**

如果端口被占用，修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
    - "8125:8000"  # 修改本地端口
```

2. **API 密钥错误**

检查 `.env` 文件中的密钥是否正确：

```bash
docker compose logs langgraph-api
```

3. **构建失败**

清理 Docker 缓存后重新构建：

```bash
docker system prune -a
langgraph build -t research-assistant-image --force
```

4. **访问超时**

增加健康检查的超时时间：

```yaml
healthcheck:
    timeout: 3s  # 增加超时
    retries: 10  # 增加重试次数
```

### 查看日志

```bash
# 查看所有服务日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f langgraph-api
```

## 维护操作

### 停止服务

```bash
docker compose down
```

### 重启服务

```bash
docker compose restart
```

### 清理数据

```bash
# 停止并删除所有容器和数据
docker compose down -v
```

### 更新镜像

```bash
# 重新构建镜像
langgraph build -t research-assistant-image --force

# 重启服务
docker compose --env-file .env up -d --force-recreate
```

## 性能优化

### 并行处理

系统使用 **Map-Reduce 模式** 并行处理多个访谈，显著提高效率：

**Map 阶段**：所有分析师的访谈同时进行
- 分析师数量：建议 3-5 个（太少视角不够，太多成本高）
- 访谈轮次：当前硬编码为 2 轮（可在代码中修改）
- 每轮访谈包含：提问 → 并行搜索（Web + Wikipedia）→ 回答

**Reduce 阶段**：报告生成也是并行的
- 引言、主体、结论三部分同时生成
- 最后组装成完整报告

**性能建议**：
- 3个分析师 × 2轮访谈 = 约 6 次 LLM 调用（访谈） + 3 次（小节）+ 4 次（报告）
- 总计约 13 次 LLM API 调用
- 预计耗时：3-5 分钟（取决于 API 响应速度）

### 资源配置

在 `docker-compose.yml` 中配置资源限制：

```yaml
langgraph-api:
    deploy:
        resources:
            limits:
                cpus: '2'
                memory: 4G
            reservations:
                cpus: '1'
                memory: 2G
```

## 安全建议

1. **API 密钥管理**
   - 不要在代码中硬编码密钥
   - 使用环境变量或密钥管理服务
   - 定期轮换密钥

2. **网络隔离**
   - 在生产环境中使用专用网络
   - 配置防火墙规则
   - 使用 HTTPS/TLS 加密

3. **访问控制**
   - 实施身份验证和授权
   - 使用 API 网关
   - 监控和日志记录

## 扩展开发

### 1. 自定义分析师生成逻辑

修改 `research_assistant.py` 中的 `analyst_instructions` 提示词模板：

```python
# 位置：第 169 行左右
analyst_instructions = """你需要创建一组 AI 分析师人设。请严格遵循以下指引：

1. 先审阅研究主题：
{topic}

2. 根据特定领域（如医疗、金融、技术）定制分析师角色
3. 确保分析师视角多样化且互补
4. 为每个分析师设定明确的关注点和专业背景
...
"""
```

### 2. 添加新的检索源

在访谈子图中添加新的检索节点：

```python
def search_custom_source(state: InterviewState):
    """
    自定义检索源（如企业内部知识库）
    """
    # 1. 生成搜索查询
    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke([search_instructions] + state['messages'])
    
    # 2. 执行检索
    search_docs = your_custom_search_api(search_query.search_query)
    
    # 3. 格式化结果
    formatted_docs = "\n\n---\n\n".join([
        f'<Document source="{doc.source}"/>\n{doc.content}\n</Document>'
        for doc in search_docs
    ])
    
    return {"context": [formatted_docs]}

# 在访谈子图中添加节点
interview_builder.add_node("search_custom", search_custom_source)
interview_builder.add_edge("ask_question", "search_custom")
interview_builder.add_edge("search_custom", "answer_question")
```

### 3. 调整访谈轮次

修改 `route_messages` 函数中的轮次限制：

```python
# 位置：第 641 行左右
def route_messages(state: InterviewState, name: str = "expert"):
    messages = state["messages"]
    max_num_turns = state.get('max_num_turns', 3)  # 改为 3 轮或更多
    # ...
```

### 4. 自定义报告格式

修改报告生成的提示词模板和后处理逻辑：

```python
# 修改 section_writer_instructions（第 256 行左右）
section_writer_instructions = """你是一名资深技术写作者。

你的任务是基于一组来源文档，撰写一段简洁、易读的报告小节。

# 自定义格式要求：
- 使用特定的行业术语
- 添加数据可视化建议
- 包含关键指标和KPI
...
"""

# 修改 finalize_report 函数（第 840 行左右）
def finalize_report(state: ResearchGraphState):
    """自定义报告组装逻辑"""
    # 添加封面页
    # 添加目录
    # 添加执行摘要
    # ... 自定义格式
```

### 5. 禁用人机协同中断

如需自动执行整个流程，修改编译配置：

```python
# 位置：第 1038 行左右
graph = builder.compile(
    # interrupt_before=['human_feedback'],  # 注释掉此行
    checkpointer=memory
)
```

## 参考资源

- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [LangGraph Platform 部署](https://langchain-ai.github.io/langgraph/cloud/)
- [LangSmith 追踪](https://docs.smith.langchain.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题，请联系开发团队或提交 Issue。

