# MCP 天气工具演示

这个项目演示了如何使用 Model Context Protocol (MCP) 创建一个客户端-服务器架构，让 AI 模型可以通过工具获取实时天气信息。

## 项目介绍

本项目是一个基于 MCP（Model Context Protocol）的入门级 Demo，用于帮助开发者理解和使用 MCP 技术。项目展示了如何创建 MCP 服务器和客户端，以及如何实现服务器与客户端之间的交互。

MCP 是一种开放协议，允许大语言模型（如 Claude）与外部系统安全地交互，提供工具、数据访问以及环境信息。通过 MCP，AI 模型可以更加安全、高效地处理需要与外部系统集成的任务。

### 项目特点

- 简单易懂的 MCP 服务器实现
- 功能完整的 MCP 客户端示例
- 基于和风天气 API 的实际应用场景
- 详细的代码注释和文档说明
- 完整的部署和使用指南

### MCP 通信模式

在 Model Context Protocol 中，stdio (Standard Input/Output，标准输入输出) 和 sse (Server-Sent Events，服务器发送事件) 是两种不同的通信模式，它们在数据如何交换和交互类型方面存在显著差异。

**`stdio` (标准输入/输出) 模式：**

* 主要用于**本地执行**，就像在命令行运行脚本一样，AI 通过标准输入给脚本指令，脚本通过标准输出直接返回结果。
* 它适合集成**已有的本地工具**，设置简单，延迟低，安全性较高（因不暴露网络）。

**`sse` (服务器发送事件) 模式：**

* 基于 **Web 技术 (HTTP)**，AI 通过网络连接与工具服务进行交互，工具服务可以持续地将更新“推送”给 AI。
* 它适合需要**网络访问、远程部署或多用户共享**的工具，更具可扩展性，但设置略复杂并需考虑网络安全。

**简单来说：**

* 想让 AI **在本地电脑上直接运行和使用工具**，就像操作本地文件一样，用 `stdio`。
* 想让 AI **通过网络（即使是本地网络）访问一个工具服务**，或者这个工具需要被多个应用或用户使用，用 `sse`。

## 项目架构

项目分为以下主要部分：

1. **MCP 服务器**：提供天气相关工具，包括获取天气预警和天气预报功能
2. **MCP 客户端**：连接服务器，发送工具调用请求，处理返回结果
3. **MCP Inspector**：用于调试和测试 MCP 服务器，提供可视化界面

### 技术栈

- **编程语言**：Python 3.10.18 ; Nodejs 22.14.0 ; Npm 10.9.2
- **部署环境**：Ubuntu 22.04
- **核心依赖**：
  - MCP SDK 1.17.0
  - HTTPX 库（HTTP 客户端）
  - 异步编程（asyncio）
- **调试工具**：
  - MCP Inspector (Node.js)

### 项目结构

```
mcp-demo/
│
├── server/                    # 服务器实现
│   └── weather_server.py      # 天气信息服务器
│
├── client/                          # 客户端实现
│   └── mcp_client.py                # MCP 客户端
│   └── mcp_client_deepseek.py       # DeepSeek MCP 客户端（支持对话）
│   └── mcp_client_langchain_chat.py # DeepSeek MCP 客户端（支持LangChain集成）
│
├── requirements.txt           # 项目依赖
└── README.md                  # 项目文档
```

### 系统交互图

```
┌─────────────┐ stdio/sse    ┌──────────────┐
│             │◄────────────►│              │
│  MCP 客户端  │                MCP 服务器   │
│             │              │              │
└─────────────┘              └──────────────┘
                                   ▲
                                   │
                              调试 │
                                   │
                                   ▼
                            ┌─────────────┐
                            │             │
                            │MCP Inspector│
                            │             │
                            └─────────────┘
```

## 功能介绍

本项目提供以下功能：

1. **天气预警查询**：获取城市ID或经纬度位置的天气灾害预警信息
2. **天气预报查询**：根据城市ID或经纬度位置获取详细的天气预报

### 服务器实现说明

服务器实现提供了两个主要工具：

- **get_weather_warning**：获取指定城市ID或经纬度的天气灾害预警
- **get_daily_forecast**：获取指定城市ID或经纬度的天气预报

这些工具通过和风天气（QWeather）API 获取实时数据。

### 和风天气 API 注册与使用

要使用本项目，需要先注册和风天气开发者账号并获取 API Key：

1. **注册和风天气开发者账号**：
   - 访问 [和风天气开发服务](https://dev.qweather.com/)
   - 点击"注册"，按照提示完成账号注册

2. **创建项目并获取 API Key**：
   - 登录开发者控制台
   - 点击"项目管理" -> "创建项目"
   - 填写项目名称、创建凭据
   - 创建成功后，在项目详情页可以获取 API Key
  ![和风天气API Key](./doc/img/qweather01.png)

3. **开发者的API Host**：
   - 登录开发者控制台
   - 点击"头像" -> "设置"，或直接访问https://console.qweather.com/setting?lang=zh
   - 查看API Host
  ![和风天气API Host](./doc/img/qweather02.png) 

4. **API 使用说明**：
   - 免费版API有调用次数限制，详情请参考[和风天气定价页面](https://dev.qweather.com/price/)
   - 支持通过城市ID或经纬度坐标查询天气信息
   - 城市ID可通过[和风天气城市查询API](https://dev.qweather.com/docs/api/geoapi/)获取

5. **和风天气API测试**：

```bash
curl --compressed \
-H "X-QW-Api-Key: XXX" \
'https://XXX/v7/weather/now?location=101010100'
```

### 客户端实现说明

客户端提供了一个简单的命令行界面，支持以下操作：

- 列出可用工具及其描述
- 调用工具并传递参数
- 显示工具执行结果
- 提供帮助信息


## 文档
1. [MCP实战入门：让AI模型获取实时天气信息](https://mp.weixin.qq.com/s/cJhHf7caaezehEff2GSY_A)
2. [MCP实战进阶：集成DeepSeek模型与MCP的天气信息助手](https://mp.weixin.qq.com/s/1YIYRVw8yF1zeeLtmnhtYQ)
3. [MCP实战高阶：借助LangChain快速打造MCP天气助手](https://mp.weixin.qq.com/s/Qq3C85Bi3NHDQ9MnnBZvZQ)

## 部署说明

### 环境要求

- Python 3.10.18
- Ubuntu 22.04 操作系统

### 安装步骤

1. **安装依赖**：

```bash
pip install -r requirements.txt
```

2. **设置和风天气 API Key 和 API Host**：
复制`.env.example`来创建 `.env` 文件并添加以下配置：
```bash
### 和风天气API配置(参考https://dev.qweather.com/)
QWEATHER_API_BASE=
QWEATHER_API_KEY=
```

## 运行方式

### 方法一： 使用 MCP Inspector调试：

MCP Inspector 是一个可视化工具，可帮助调试和测试 MCP 服务器。要使用 MCP Inspector：

1. **安装 MCP Inspector**：

```bash
npm install -g @modelcontextprotocol/inspector
```

2. **使用 MCP Inspector 调试服务器**：

推荐使用简化命令 `mcp dev`：

```bash
pip install mcp[cli]
mcp dev server/weather_server.py
```

执行过程
```
(agent101) root@fly:/Agent101/code/AIAgent101/02-agent-llm-mcp/mcp-demo# mcp dev server/weather_server.py
Starting MCP inspector...
⚙️ Proxy server listening on localhost:6277
🔑 Session token: e291634cdaa8ab8b6601b61bd228cff4245a492db8f35fad431071cd1dc2f38f
   Use this token to authenticate requests or set DANGEROUSLY_OMIT_AUTH=true to disable auth

🚀 MCP Inspector is up and running at:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=e291634cdaa8ab8b6601b61bd228cff4245a492db8f35fad431071cd1dc2f38f

🌐 Opening browser...

```

或者使用 npx（如果未全局安装）：

```bash
npx @modelcontextprotocol/inspector python server/weather_server.py
```

3. **在浏览器中访问 Inspector**：

默认情况下，Inspector UI 运行在 http://localhost:6274，而 MCP 代理服务器运行在端口 6277。

4. **通过 Inspector 调试**：
   - 查看可用工具及其描述
   ![查看可用工具及其描述](./doc/img/MCP%20Inspector01.png)
   - 查询北京未来3天天气
   ![查询北京未来3天天气](./doc/img/MCP%20Inspector02.png)
   - 查询北京灾害预警
   ![查询北京灾害预警](./doc/img/MCP%20Inspector03.png)

> **提示**：MCP Inspector 提供了更直观的界面来测试和调试 MCP 服务器，特别适合开发和调试复杂工具。


### 方法二：使用Python启动客户端

```bash
python client/mcp_client.py
```



### 方法三：使用Python启动客户端（DeepSeek）

#### DeepSeek MCP 客户端

这是一个基于模型上下文协议 (Model Context Protocol - MCP) 的客户端实现，集成了 DeepSeek API 来处理用户查询。该客户端能够连接到 MCP 服务器，利用 DeepSeek 的大语言模型能力来理解用户查询，并通过 MCP 工具（如天气查询/灾害预警）来执行相应的操作并返回结果。

##### 功能特点

* **MCP 集成**: 与兼容 MCP 协议的服务器建立连接和通信。
* **DeepSeek 驱动**: 使用 DeepSeek API (通过 OpenAI SDK 兼容接口) 处理自然语言查询。
* **工具调用**: 支持根据用户意图自动调用 MCP 服务器上定义的工具（例如 `get_daily_forecast`, `get_weather_warning`）。
* **交互式体验**: 提供一个简单的命令行界面 (CLI) 进行交互式问答。
* **稳健性**: 包含错误处理（连接、API 调用、工具执行）和资源管理（确保连接正确关闭）。
* **可配置**: 通过环境变量轻松配置 API 密钥、URL 和模型。
* **可扩展**: 易于通过修改系统提示或在 MCP 服务器端添加新工具来扩展功能。

在运行客户端之前，需要配置以下环境变量。修改`mcp-demo`文件夹下名为 `.env` 的文件(如果没有，请先复制`.env.example`来创建 `.env` 文件)：

```dotenv
# .env 文件内容示例
DEEPSEEK_API_KEY=sk-xxxxxxxxx                # DeepSeek API 密钥
DEEPSEEK_BASE_URL=https://api.deepseek.com   # DeepSeek API 的基础 URL
DEEPSEEK_MODEL=deepseek-chat                 # 使用的 DeepSeek 模型名称
```

#### 启动客户端
```bash
python client/mcp_client_deepseek.py
```


### 方法四：使用Python启动客户端（DeepSeek）[LangChain版]

主要是： 借助LangChain一个新的开源项目 `langchain-mcp-adapters`，将MCP服务器集成到 LangChain中

LangChain版本相比原生DeepSeek版本在MCP开发中的主要优势：

1. **更简洁的代理创建流程**：LangChain版本使用`create_react_agent`函数直接创建代理，简化了代码复杂度：
   ```python
   agent = create_react_agent(
       model=self.llm_client,  
       tools=tools,
       prompt=prompt
   )
   ```
   而DeepSeek直接实现需要手动处理整个工具调用循环。

2. **自动化的工具处理**：LangChain版本使用`load_mcp_tools`函数自动适配MCP工具，省去了工具格式转换的工作：
   ```python
   tools = await load_mcp_tools(self.session)
   ```
   对比DeepSeek版本需要手动将MCP工具转换为OpenAI格式：
   ```python
   available_tools = [tool.to_openai_format() for tool in tools]
   ```

3. **内置的ReAct推理能力**：LangChain版本利用了该框架的ReAct代理能力，可以自动执行"思考-行动-观察"循环，而无需手动管理对话历史和工具调用次数。

4. **简化的消息管理**：LangChain处理模型消息和工具调用结果的逻辑更加抽象化，不需要手动构建完整的消息历史。DeepSeek版本需要手动管理消息传递和工具调用的过程。

5. **扩展性更好**：LangChain提供了标准化的工具接口，可以更容易地扩展到其他模型或添加新工具，同时保持代码结构一致。

6. **减少错误处理负担**：LangChain内置了更多的错误处理机制，而DeepSeek版本需要开发者手动实现各种错误处理代码。

7. **更精简的执行循环**：DeepSeek版本需要手动实现多轮工具调用循环(max_tool_turns)，而LangChain版本通过代理自动处理这一过程。

8. **结果展示更丰富**：LangChain版本会自动记录并可视化工具调用过程和结果，方便调试和优化：
   ```python
   for message in agent_response['messages']:
       print(f"\nTool: {message.name}")
       print(f"Content:\n{message.content}")
   ```

总结来说，使用LangChain框架开发MCP客户端的主要优势在于：代码更简洁、抽象层次更高、工具处理更自动化、扩展性更好，并且减少了开发者需要手动管理的复杂逻辑，特别是在多轮工具调用和消息处理方面。


在运行客户端之前，需要配置以下环境变量。修改`mcp-demo`文件夹下名为 `.env` 的文件(如果没有，请先复制`.env.example`来创建 `.env` 文件)：

```dotenv
# .env 文件内容示例
DEEPSEEK_API_KEY=sk-xxxxxxxxx                # DeepSeek API 密钥
DEEPSEEK_BASE_URL=https://api.deepseek.com   # DeepSeek API 的基础 URL
DEEPSEEK_MODEL=deepseek-chat                 # 使用的 DeepSeek 模型名称
```

#### 启动客户端
```bash
# 具备聊天交互
python client/mcp_client_langchain_chat.py
```


## 常见问题

### 服务器无法启动

- 确保已安装所有依赖
- 检查 Python 版本是否 3.10 或更高版本
- 检查服务器文件权限是否正确
- 确保 QWEATHER_API_KEY 环境变量已正确设置

### API 请求失败

- 确保网络连接正常
- 检查 API Key 是否有效
- 和风天气免费版 API 有请求次数限制
- 检查请求参数格式是否正确

## 使用 MCP Inspector 调试与故障排除

MCP Inspector 是开发和调试 MCP 服务器的重要工具，提供了直观的可视化界面，帮助开发者理解和解决问题。

### Inspector 的主要功能

1. **实时工具调用**：
   - 通过界面直接调用 MCP 工具
   - 可视化参数表单，避免语法错误
   - 查看格式化的执行结果

2. **请求历史记录**：
   - 跟踪所有工具调用历史
   - 复制和重放之前的请求
   - 对比不同参数下的执行结果

3. **错误分析**：
   - 详细的错误消息和堆栈跟踪
   - 突出显示参数验证错误
   - 显示请求/响应时间，帮助性能分析

4. **流式响应可视化**：
   - 查看支持流式传输的工具的实时输出
   - 分析流式传输过程中的延迟

### 常见调试场景

#### 1. 参数验证错误

当工具参数格式不正确时：

```bash
npx @modelcontextprotocol/inspector python server/weather_server.py
```

在 Inspector 中：
1. 选择工具（如 `get_daily_forecast`）
2. 故意提供错误格式的参数（如字符串而非数字）
3. 执行后，Inspector 会显示详细的验证错误

#### 2. API 集成问题

当外部 API 调用失败时：

```bash
npx @modelcontextprotocol/inspector python server/weather_server.py
```

在 Inspector 中：
1. 调用 `get_weather_warning` 或 `get_daily_forecast` 工具
2. 检查网络请求错误信息
3. 分析响应码和错误消息

#### 3. 性能分析

分析工具执行时间：

```bash
npx @modelcontextprotocol/inspector python server/weather_server.py
```

在 Inspector 中：
1. 调用目标工具多次，使用不同参数
2. 分析每次调用的执行时间
3. 识别性能瓶颈

### 调试优秀做法

1. **先用 Inspector，再集成客户端**：
   - 在开发新工具时，先用 Inspector 测试和完善
   - 确保工具正常工作后再集成到客户端

2. **保存常用测试用例**：
   - 使用 Inspector 的"保存请求"功能
   - 创建不同场景的测试用例集

3. **使用 CLI 模式进行自动化测试**：
   ```bash
   npx @modelcontextprotocol/inspector --cli python server/weather_server.py --method tools/call --tool-name get_weather_warning --tool-arg location=101010100
   ```

4. **对比服务器版本**：
   - 使用相同参数测试不同版本的服务器实现
   - 分析性能和行为差异

通过有效使用 MCP Inspector，可以显著提高开发效率，减少调试时间，并确保 MCP 服务器的稳定性和可靠性。

## 扩展与优化

1. **添加更多工具**：可以扩展服务器添加更多工具，如历史天气数据查询、未来几天预报等
2. **支持更多数据源**：集成其他天气 API，提供全球天气信息
3. **改进用户界面**：开发图形用户界面，提供更直观的操作体验
4. **添加用户认证**：增加安全措施，实现用户认证和权限控制
5. **优化性能**：添加缓存机制，减少 API 请求次数


