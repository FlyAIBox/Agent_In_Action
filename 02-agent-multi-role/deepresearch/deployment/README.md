# 深度研究助手 - 容器化部署指南

本文档介绍如何使用 LangGraph Platform 部署深度研究助手（Deep Research Assistant）系统。

## 系统概述

深度研究助手是一个基于 LangGraph 的智能研究系统，具备以下核心功能：

### 核心功能

1. **分析师团队生成**
   - 根据研究主题自动生成多位AI分析师
   - 支持人类反馈进行分析师调整
   - 每位分析师负责特定的研究视角

2. **并行访谈系统**
   - 分析师与专家进行多轮深度访谈
   - 支持网络搜索和百科检索
   - 智能提问和回答生成

3. **报告生成**
   - 自动整合多个分析师的研究成果
   - 生成结构化的研究报告
   - 包含引言、主体内容、结论和引用

4. **工作流架构**
   - 使用 Map-Reduce 模式并行处理
   - 支持人机协同（Human-in-the-loop）
   - 完整的状态管理和检查点机制

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    深度研究助手系统                          │
├─────────────────────────────────────────────────────────────┤
│  1. 分析师生成 → 2. 人机协同 → 3. 并行访谈 → 4. 报告生成   │
└─────────────────────────────────────────────────────────────┘
         ↓                ↓                ↓           ↓
    ┌────────┐      ┌────────┐      ┌────────┐  ┌────────┐
    │OpenAI  │      │Memory  │      │Tavily  │  │百度百科│
    │GPT-4o  │      │Store   │      │Search  │  │Loader  │
    └────────┘      └────────┘      └────────┘  └────────┘
```

## 技术栈

- **LangGraph**: 0.6.7 - 智能体工作流框架
- **LangChain**: 0.3.27 - 大模型应用框架
- **OpenAI GPT-4o**: 语言模型
- **Tavily Search**: 网络搜索服务
- **百度百科**: 知识检索
- **PostgreSQL**: 状态持久化存储
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
cd 01-agent-build/6-DeepResearchAssistant/deployment

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

# 连接到部署
client = get_client(url="http://localhost:8124")

# 创建线程
thread = await client.threads.create()

# 启动研究
config = {
    "configurable": {
        "topic": "人工智能在医疗领域的应用",
        "max_analysts": 3
    }
}

# 执行研究流程
async for chunk in client.runs.stream(
    thread["thread_id"],
    "research_assistant",
    input=None,
    config=config,
    stream_mode="values"
):
    # 处理流式输出
    if "final_report" in chunk:
        print(chunk["final_report"])
```

### Remote Graph 示例

```python
from langgraph.pregel.remote import RemoteGraph

# 连接到远程图
remote_graph = RemoteGraph("research_assistant", url="http://localhost:8124")

# 配置研究参数
config = {
    "configurable": {
        "topic": "区块链技术的发展趋势",
        "max_analysts": 3
    }
}

# 执行研究
result = await remote_graph.ainvoke({
    "topic": "区块链技术的发展趋势",
    "max_analysts": 3
}, config=config)

# 获取最终报告
print(result["final_report"])
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

#### configuration.py

定义可配置的参数：

```python
@dataclass(kw_only=True)
class Configuration:
    topic: str = "人工智能的发展趋势"
    max_analysts: int = 3
    max_interview_turns: int = 2
    enable_human_feedback: bool = True
```

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

系统使用 Map-Reduce 模式并行处理多个访谈，提高效率：

- 分析师数量：建议 2-5 个
- 访谈轮次：建议 2-3 轮
- 并发请求：根据 API 限制调整

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

### 自定义分析师生成

修改 `research_assistant.py` 中的提示词模板：

```python
analyst_instructions = """你需要创建一组 AI 分析师人设。
根据特定领域（如医疗、金融）定制分析师角色...
"""
```

### 添加新的检索源

实现新的检索节点：

```python
def search_custom_source(state: InterviewState):
    """自定义检索源"""
    # 实现检索逻辑
    return {"context": [formatted_docs]}
```

### 调整报告格式

修改报告生成的提示词和后处理逻辑。

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

