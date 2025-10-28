# 快速启动指南

这是深度研究助手的快速部署和使用指南，5分钟内即可完成部署。

## 📋 前置要求

- ✅ Docker 和 Docker Compose
- ✅ Python 3.11+
- ✅ LangGraph CLI
- ✅ OpenAI API 密钥

## 🚀 快速部署（5步）

### 第1步：安装 LangGraph CLI

```bash
pip install langgraph-cli==0.4.2
```

### 第2步：配置环境变量

```bash
# 复制环境变量模板
cp .env-example .env

# 编辑 .env 文件，填入你的 API 密钥
# 必需：OPENAI_API_KEY
# 可选：TAVILY_API_KEY, LANGSMITH_API_KEY
```

### 第3步：构建 Docker 镜像

```bash
# 在 deployment 目录下执行
langgraph build -t research-assistant-image
```

> 💡 提示：首次构建可能需要几分钟

### 第4步：启动服务

```bash
docker compose --env-file .env up -d
```

等待服务启动（约30秒），你会看到三个容器：
- ✅ langgraph-redis (端口 6380)
- ✅ langgraph-postgres (端口 5433)
- ✅ langgraph-api (端口 8124)

### 第5步：验证部署

```bash
# 方法1：访问API文档
# 浏览器打开: http://localhost:8124/docs

# 方法2：运行测试脚本
python test_connection.py
```

## 🎯 基本使用

### 方式1：使用 Python SDK

```python
from langgraph_sdk import get_client

# 连接到服务
client = get_client(url="http://localhost:8124")

# 创建线程
thread = await client.threads.create()

# 启动研究
async for event in client.runs.stream(
    thread["thread_id"],
    "research_assistant",
    input={
        "topic": "人工智能在医疗领域的应用",
        "max_analysts": 3
    },
    stream_mode="values"
):
    if "final_report" in event:
        print(event["final_report"])
```

### 方式2：使用 Remote Graph

```python
from langgraph.pregel.remote import RemoteGraph

# 创建远程图实例
remote_graph = RemoteGraph(
    "research_assistant", 
    url="http://localhost:8124"
)

# 执行研究
result = await remote_graph.ainvoke({
    "topic": "区块链技术的发展趋势",
    "max_analysts": 3
})

print(result["final_report"])
```

### 方式3：使用 LangGraph Studio

在浏览器中访问：
```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8124
```

## 📊 配置参数

在调用时可以通过 `config` 参数配置：

```python
config = {
    "configurable": {
        "topic": "研究主题",           # 研究的主题
        "max_analysts": 3,             # 分析师数量（建议2-5）
        "max_interview_turns": 2,      # 访谈轮次（建议2-3）
        "enable_human_feedback": True  # 是否启用人机协同
    }
}
```

## 🔧 常用命令

### 查看服务状态
```bash
docker compose ps
```

### 查看日志
```bash
docker compose logs -f langgraph-api
```

### 重启服务
```bash
docker compose restart
```

### 停止服务
```bash
docker compose down
```

### 清理数据
```bash
docker compose down -v
```

## 🐛 常见问题

### Q1: 端口被占用

**错误**: `Error starting userland proxy: listen tcp4 0.0.0.0:8124: bind: address already in use`

**解决**: 修改 `docker-compose.yml` 中的端口映射
```yaml
ports:
    - "8125:8000"  # 将 8124 改为其他端口
```

### Q2: API 密钥错误

**错误**: `AuthenticationError: Invalid API key`

**解决**: 检查 `.env` 文件中的 API 密钥是否正确

### Q3: 构建失败

**错误**: `Error building image`

**解决**: 清理 Docker 缓存后重新构建
```bash
docker system prune -a
langgraph build -t research-assistant-image
```

### Q4: 连接超时

**错误**: `Connection timeout`

**解决**: 
1. 检查服务是否启动：`docker compose ps`
2. 查看日志：`docker compose logs -f`
3. 增加健康检查超时时间

## 📚 进阶使用

### 人机协同模式

```python
# 1. 启动研究到分析师生成阶段
async for event in client.runs.stream(...):
    if "analysts" in event:
        print("生成的分析师：", event["analysts"])
        break

# 2. 提供人类反馈
await client.threads.update_state(
    thread["thread_id"],
    {"human_analyst_feedback": "添加一位金融分析师"},
    as_node="human_feedback"
)

# 3. 继续执行
async for event in client.runs.stream(...):
    if "final_report" in event:
        print(event["final_report"])
```

### 自定义搜索源

编辑 `research_assistant.py`，添加自定义检索节点：

```python
def search_custom_source(state: InterviewState):
    """自定义检索源"""
    # 实现你的检索逻辑
    return {"context": [formatted_docs]}

# 在 interview_builder 中添加节点
interview_builder.add_node("search_custom", search_custom_source)
interview_builder.add_edge("ask_question", "search_custom")
```

## 📖 完整文档

详细文档请参考：
- [README.md](./README.md) - 完整部署文档
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [LangGraph Platform](https://langchain-ai.github.io/langgraph/cloud/)

## 💡 提示

1. **首次使用建议**：先运行 `test_connection.py` 确保部署正常
2. **性能优化**：根据 API 限制调整分析师数量和访谈轮次
3. **成本控制**：使用 LangSmith 监控 token 消耗
4. **调试技巧**：启用 `LANGSMITH_TRACING` 查看详细执行过程

## 🆘 获取帮助

如遇问题：
1. 查看日志：`docker compose logs -f`
2. 运行测试：`python test_connection.py`
3. 参考完整文档：[README.md](./README.md)
4. 提交 Issue

---

祝你使用愉快！🎉

