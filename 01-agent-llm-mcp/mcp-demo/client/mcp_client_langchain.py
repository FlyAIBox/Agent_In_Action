"""
# 集成 DeepSeek 的 MCP 客户端[LangChain版]
#更详细的使用方法请参考：https://github.com/langchain-ai/langchain-mcp-adapters

# 所需环境变量：
# DEEPSEEK_API_KEY：DeepSeek API 密钥 (格式：sk-xxxx...)
# DEEPSEEK_BASE_URL：DeepSeek API 基础 URL (https://api.deepseek.com)
# DEEPSEEK_MODEL：DeepSeek 模型名称 (例如 deepseek-chat)

Author: FlyAIBox
Date: 2025.10.11
"""
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import logging

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt import chat_agent_executor
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 优先从环境变量加载API密钥等信息
load_dotenv()

# 配置和风天气API环境变量（如果在环境中不存在）
if not os.getenv("QWEATHER_API_KEY"):
    os.environ["QWEATHER_API_KEY"] = "XXX"  # 请替换为实际的API密钥
if not os.getenv("QWEATHER_API_BASE"):
    os.environ["QWEATHER_API_BASE"] = "https://n83tefhk3u.re.qweatherapi.com/v7"

# 配置 ChatOpenAI
model = ChatOpenAI(
    api_key="XXX",
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0
)

async def main():
    # 确定服务器路径
    server_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "server",
        "weather_server.py"
    )

    # 检查服务器文件是否存在
    if not os.path.exists(server_path):
        logger.error(f"错误: 服务器文件不存在: {server_path}")
        return

    server_params = StdioServerParameters(
        command="python",
        args=[server_path],
    )

    try:
        logger.info("正在启动客户端连接...")
        async with stdio_client(server_params) as (read, write):
            logger.info("成功建立客户端连接")
            
            async with ClientSession(read, write) as session:
                # Initialize the connection
                logger.info("正在初始化会话...")
                await session.initialize()
                logger.info("会话初始化成功")

                # Get tools
                logger.info("正在加载MCP工具...")
                tools = await load_mcp_tools(session)
                logger.info(f"成功加载工具: {[tool.name for tool in tools]}")

                # 创建提示模板
                prompt = SystemMessage(content=""""You are a helpful assistant specializing in weather information.\n
                                    You have access to the MCP Weather Server tool with the following functions:\n
                                    - get_weather_warning(city_id=None, latitude=None, longitude=None): Retrieves weather disaster warnings for a specified city ID or coordinates.\n
                                    - get_daily_forecast(city_id=None, latitude=None, longitude=None): Retrieves the multi-day weather forecast for a specified city ID or coordinates.\n
                                    \n
                                    Core Instructions:\n
                                    1.  **Carefully analyze the user's request**: Understand all components of the user's query. Determine if the user needs weather warning information, weather forecast information, or both.\n
                                    2.  **Identify Information Needs**:\n
                                        * If the user only asks for warnings (e.g., \Are there any warnings in Beijing?\), only use `get_weather_warning`.\n
                                        * If the user only asks for the forecast (e.g., \What's the weather like in Beijing tomorrow?\), only use `get_daily_forecast`.\n
                                        * **If the user's question includes multiple aspects**, such as asking about **warning status** and also asking **if it's suitable for a certain activity** (which implies a query about future weather, like \Have there been high temperature warnings in Beijing in the last week? Is it suitable for outdoor activities?\), you need to **call both tools sequentially**.\n
                                    3.  **Call Tools as Needed**:\n
                                        * **Prioritize getting warning information**: If warning information is needed, first call `get_weather_warning`.\n
                                        * **Get the weather forecast**: If the user mentions a specific time period (e.g., \weekend\, \next three days\, \next week\) or asks about activity suitability (which typically concerns the next few days), call `get_daily_forecast` to get the forecast for the corresponding period. For vague phrases like \last week\ or \recently\, interpret it as asking about *current* conditions and the *upcoming* few days (covered by the forecast). For questions like \Is it suitable for outdoor activities?\, you should get the forecast for at least the next 2-3 days (e.g., today, tomorrow, the day after tomorrow, or the upcoming weekend) to support your judgment.\n
                                        * **Ensure tool call order**: When multiple tools need to be called, they should be called in a logical sequence. For example, first get the warning, then get the forecast. Wait for one tool to finish executing before deciding whether to call the next tool or generate a response.\n
                                    4.  **Information Integration and Response**:\n
                                        * After obtaining all necessary information (warning, forecast), you **must synthesize and analyze this information**.\n
                                        * **Completely answer the user's question**: Ensure you answer all parts of the user's query.\n
                                        * **Provide advice**: If the user asks about activity suitability, based on the retrieved warning status and forecast information (temperature, weather condition - clear/rainy, wind strength, etc.), provide a clear, data-supported recommendation (e.g., \Currently there are no high temperature warnings, but it's expected to rain this weekend, so it's not very suitable for outdoor activities,\ or \It will be sunny for the next few days with no warnings, suitable for outdoor activities.\).\n
                                    5.  **Tool Usage Details**:\n
                                        * When using the tools, retain the full context of the user's original question.\n
                                        * Unless explicitly requested by the user, do not insert specific times of day (e.g., \3 PM\) into the search query or your response.\n
                                        * When city information is needed, if the user provides a city name (e.g., \Beijing\), use the corresponding `city_id` (e.g., Beijing's city_id might be '101010100').\n                      
                                  """)

                # Create and run the agent
                logger.info("正在创建agent...")
                agent = create_react_agent(
                    model=model,  
                    tools=tools,
                    prompt=prompt
                )
                logger.info("Agent创建成功")

                # 发送查询
                logger.info("正在发送天气查询...")
                agent_response = await agent.ainvoke({
                    "messages": "最近一周郑州有没有高温或大风预警？周末适合户外活动吗？"
                })

                # 打印响应
                logger.info("\nAgent Response:")
                print(agent_response)

                # 遍历消息列表并打印 ToolMessage 的 content
                if 'messages' in agent_response:
                    print("\n--- Tool Message Contents ---")
                    for message in agent_response['messages']:
                        print(f"\nTool: {message.name}") # 可以选择打印工具名称
                        print(f"Content:\n{message.content}")
                        print("-" * 20) # 分隔不同 ToolMessage 的内容

    except Exception as e:
        logger.error(f"运行过程中发生错误: {str(e)}", exc_info=True)
        # 如果是TaskGroup相关的错误，打印更详细的信息
        if "TaskGroup" in str(e) and hasattr(e, "__cause__"):
            logger.error(f"TaskGroup错误详情: {str(e.__cause__)}")

if __name__ == "__main__":
    asyncio.run(main())