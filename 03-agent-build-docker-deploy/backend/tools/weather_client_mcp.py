"""
# 集成 DeepSeek 的 MCP 客户端
#参考官方案例：https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py


# 本模块实现了一个模型上下文协议（MCP）客户端，该客户端使用大语言模型的 API
# 来处理查询并与 MCP 工具进行交互。它演示了如何：
# 1. 连接到 MCP 服务器
# 2. 使用大语言模型的 API 来处理查询
# 3. 处理工具调用和响应
# 4. 维护一个交互式聊天循环


Author: FlyAIBox
Date: 2025.10.11
"""

import asyncio
import logging
import os
import aiohttp
import json
from typing import Optional, Dict, Any, List
from contextlib import AsyncExitStack
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 配置详细日志记录器
def setup_weather_client_logger():
    """设置天气客户端日志记录器"""
    logger = logging.getLogger('weather_client')
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # 确保日志目录存在
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 创建文件处理器
        file_handler = logging.FileHandler('logs/backend.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 设置详细日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
    
    return logger

# 创建全局日志记录器
logger = setup_weather_client_logger()

load_dotenv()


def _resolve_mcp_server_path() -> str:
    """解析 MCP 天气服务器脚本路径，尝试多个候选位置并返回首个存在的路径。"""
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates = [
        os.path.join(backend_dir, "server", "weather_server_mcp.py"),
        os.path.join(backend_dir, "server", "weather_server.py"),
        os.path.join(backend_dir, "tools", "weather_server_mcp.py"),
        os.path.join(backend_dir, "tools", "weather_server.py"),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            logger.info(f"MCP 服务器脚本已定位: {candidate}")
            return candidate
    raise FileNotFoundError(
        "找不到MCP天气服务器文件，已检查: " + ", ".join(candidates)
    )

class Configuration:
    """配置管理类，负责管理和验证环境变量"""
    
    def __init__(self) -> None:
        """初始化配置并加载环境变量"""
        self.load_env()
        self._validate_env()
        
    @staticmethod
    def load_env() -> None:
        """从.env文件加载环境变量"""
        load_dotenv()
        
    def _validate_env(self) -> None:
        """验证必需的环境变量是否存在"""
        required_vars = ["OPENAI_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"缺少必需的环境变量: {', '.join(missing_vars)}")
    
    @property
    def api_key(self) -> str:
        """获取 DeepSeek API 密钥"""
        return os.getenv("OPENAI_API_KEY", "")
    
    @property
    def base_url(self) -> str:
        """获取 DeepSeek API 基础 URL"""
        return os.getenv("OPENAI_BASE_URL")
    
    @property
    def model(self) -> str:
        """获取 DeepSeek 模型名称"""
        return os.getenv("OPENAI_MODEL", "gpt-4o")

class Tool:
    """MCP 工具类，表示一个具有属性的工具"""
    
    def __init__(self, name: str, description: str, input_schema: Dict[str, Any]) -> None:
        """
        初始化工具
        
        Args:
            name: 工具名称
            description: 工具描述
            input_schema: 输入参数模式
        """
        self.name = name
        self.description = description
        self.input_schema = input_schema

class MCPServer:
    """MCP 服务器管理类，处理服务器连接和工具执行"""
    
    def __init__(self, server_path: str) -> None:
        """
        初始化服务器管理器
        
        Args:
            server_path: 服务器脚本路径
        """
        self.server_path = server_path
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self._cleanup_lock = asyncio.Lock()
        
    async def initialize(self) -> None:
        """初始化服务器连接，包含重试机制"""
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                logger.info(f"尝试连接 MCP 服务器 (第 {attempt + 1}/{max_retries} 次): {self.server_path}")
                if not os.path.exists(self.server_path):
                    raise FileNotFoundError(f"找不到服务器文件: {self.server_path}")
                
                server_params = StdioServerParameters(
                    command='python',
                    args=[self.server_path],
                    env=None
                )
                
                stdio_transport = await self.exit_stack.enter_async_context(
                    stdio_client(server_params)
                )
                stdio, write = stdio_transport
                
                self.session = await self.exit_stack.enter_async_context(
                    ClientSession(stdio, write)
                )
                await self.session.initialize()
                logger.info("成功连接到 MCP 服务器")
                break
                
            except Exception as e:
                logger.error(f"第 {attempt + 1}/{max_retries} 次尝试失败: {str(e)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                else:
                    raise
                    
    async def list_tools(self) -> List[Tool]:
        """获取服务器提供的可用工具列表"""
        if not self.session:
            raise RuntimeError("服务器未初始化")
            
        logger.info("请求服务器工具列表…")
        response = await self.session.list_tools()
        tools = [
            Tool(tool.name, tool.description, tool.inputSchema)
            for tool in response.tools
        ]
        logger.info(f"工具列表获取成功，数量: {len(tools)}，名称: {[t.name for t in tools]}")
        return tools
        
    async def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        retries: int = 2,
        delay: float = 1.0
    ) -> Any:
        """
        执行工具，包含重试机制
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            retries: 重试次数
            delay: 重试延迟时间（秒）
            
        Returns:
            工具执行结果
        """
        if not self.session:
            raise RuntimeError("服务器未初始化")
            
        for attempt in range(retries):
            try:
                logger.info(f"执行工具调用开始: name={tool_name}, args={arguments}, attempt={attempt + 1}/{retries}")
                result = await self.session.call_tool(tool_name, arguments)
                # 尝试记录结果摘要
                try:
                    content = getattr(result, 'content', None)
                    if content:
                        preview = str(content)[:500]
                        logger.info(f"工具调用成功: name={tool_name}, 返回内容预览(<=500 chars)={preview}")
                    else:
                        logger.info(f"工具调用成功: name={tool_name}, 返回为空或无 content 字段")
                except Exception as log_err:
                    logger.warning(f"记录工具返回摘要时出错: {log_err}")
                return result
                
            except Exception as e:
                logger.error(f"工具执行失败 (第 {attempt + 1}/{retries} 次尝试): {str(e)}")
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
                else:
                    raise
                    
    async def cleanup(self) -> None:
        """清理服务器资源"""
        async with self._cleanup_lock:
            try:
                logger.info("开始清理 MCP 服务器连接与资源…")
                await self.exit_stack.aclose()
                self.session = None
                logger.info("服务器资源清理完成")
            except Exception as e:
                logger.error(f"清理过程中出错: {str(e)}")

class MCPWeatherClient:
    """精简版 MCP 天气客户端，用于直接调用 MCP 天气工具。

    提供易用的上下文管理与方法封装，适合编程式调用而非经由 LLM 的工具编排。
    """

    def __init__(self) -> None:
        self.server: Optional[MCPServer] = None

    async def __aenter__(self) -> "MCPWeatherClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def connect(self) -> None:
        """建立到本地 MCP 天气服务器的连接。"""
        server_path = _resolve_mcp_server_path()
        logger.info(f"准备连接 MCP 天气服务器: {server_path}")
        self.server = MCPServer(server_path)
        await self.server.initialize()

    async def close(self) -> None:
        """关闭连接并清理资源。"""
        if self.server:
            await self.server.cleanup()
            self.server = None

    async def get_daily_forecast(self, location: str, days: int = 3) -> str:
        """调用 MCP 工具 `get_daily_forecast` 获取天气预报。

        参数:
            location: 位置（城市名/城市ID/经纬度）
            days: 预报天数，支持 3、7、10、15、30

        返回:
            格式化后的天气预报字符串
        """
        if not self.server:
            raise RuntimeError("MCPWeatherClient 尚未连接。请先调用 connect() 或使用 async with。")

        valid_days = {3, 7, 10, 15, 30}
        if days not in valid_days:
            logger.warning(f"无效的 days={days}，将回退为 3")
            days = 3

        # 解析位置参数，将中文城市名或拼音转换为城市ID
        arguments: Dict[str, Any] = {"location": location, "days": int(days)}
        logger.info(f"调用 get_daily_forecast，入参: location={location}, days={days}")
        result = await self.server.execute_tool("get_daily_forecast", arguments)

        # MCP 返回结果通常包含 content 列表与 Part 文本
        try:
            # result.content[0].text 形态（与上文 MCPClient.process_query 保持一致）
            text = result.content[0].text  # type: ignore[attr-defined]
            logger.info(f"get_daily_forecast 返回文本长度: {len(text)}")
            return text
        except Exception:
            # 兜底返回字符串
            fallback = str(result)
            logger.info(f"get_daily_forecast 返回非标准结构，已转为字符串，长度: {len(fallback)}")
            return fallback

async def fetch_forecast_via_mcp(location: str, days: int = 3) -> str:
    """
    通过 MCP 获取天气预报
    
    这是一个简化的接口函数，自动处理 MCP 客户端的创建、连接和清理工作。
    适用于只需要获取一次天气预报的场景。
    
    参数:
        location (str): 位置信息，支持以下格式：
                       - 中文城市名（如"北京"、"西宁"等，会自动转换为拼音再查找城市ID）
                       - 城市拼音（如"xining"表示西宁，会自动转换为城市ID）
                       - 城市ID（如"101010100"表示北京）  
                       - 经纬度坐标（如"116.41,39.92"）
        days (int): 预报天数，默认为3天，支持3、7、10、15、30天
        
    返回:
        str: 格式化的天气预报信息
        
    示例:
        >>> forecast = await fetch_forecast_via_mcp("北京", 7)        # 中文城市名
         >>> forecast = await fetch_forecast_via_mcp("beijing", 7)    # 城市拼音
        >>> forecast = await fetch_forecast_via_mcp("101010100", 7)   # 城市ID
        >>> forecast = await fetch_forecast_via_mcp("116.41,39.92", 7) # 经纬度
        >>> print(forecast)
    """
    logger.info(f"通过 MCP 工具获取天气预报: 位置={location}, 天数={days}")
    try:
        async with MCPWeatherClient() as client:
            logger.info("MCPWeatherClient 上下文已建立，开始请求预报…")
            result = await client.get_daily_forecast(location=location, days=days)
            logger.info("MCP 工具调用成功，已获得返回结果")
            return result
    except Exception as e:
        logger.error(f"MCP 工具调用失败: {str(e)}")
        raise
