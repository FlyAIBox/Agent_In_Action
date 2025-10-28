# LangGraph多智能体配置文件
"""
AI旅行规划智能体配置

这个配置文件定义了整个多智能体系统的核心参数，包括：
- OpenAI 兼容大语言模型的配置
- DuckDuckGo搜索引擎的设置
- 智能体协作的参数
- 旅行规划功能的开关

适用于大模型技术初级用户：
配置文件是AI应用的"控制中心"，通过修改这里的参数
可以调整系统的行为和性能。
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any

# 加载环境变量文件(.env)
load_dotenv()

class LangGraphConfig:
    """
    AI旅行规划智能体配置类

    这个类集中管理所有系统配置参数，包括：
    - API密钥和模型设置
    - 搜索引擎配置
    - 智能体协作参数
    - 功能开关
    """

    # OpenAI 兼容接口配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # OpenAI 风格接口密钥
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # 默认 OpenAI 基础地址
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # 默认模型，可根据网关修改

    # DuckDuckGo搜索引擎配置
    DUCKDUCKGO_MAX_RESULTS = 10        # 每次搜索的最大结果数
    DUCKDUCKGO_REGION = "zh-cn"        # 搜索区域设置为中国
    DUCKDUCKGO_SAFESEARCH = "moderate" # 安全搜索级别

    # 智能体协作配置
    MAX_ITERATIONS = 50      # 最大迭代次数
    RECURSION_LIMIT = 100    # 递归限制

    # 旅行规划功能配置
    WEATHER_SEARCH_ENABLED = True      # 启用天气搜索
    ATTRACTION_SEARCH_ENABLED = True   # 启用景点搜索
    HOTEL_SEARCH_ENABLED = True        # 启用酒店搜索
    RESTAURANT_SEARCH_ENABLED = True   # 启用餐厅搜索

    # 模型生成参数
    TEMPERATURE = 0.7    # 控制生成文本的随机性(0-1，越高越随机)
    MAX_TOKENS = 4000    # 最大生成token数
    TOP_P = 0.9         # 核采样参数，控制生成质量
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """
        获取 OpenAI 兼容模型配置

        返回用于初始化 ChatOpenAI 模型的配置字典，
        包含模型名称、接口地址和生成参数。
        """
        config: Dict[str, Any] = {
            "model": cls.OPENAI_MODEL,
            "temperature": cls.TEMPERATURE,
            "max_tokens": cls.MAX_TOKENS,
            "top_p": cls.TOP_P,
        }
        if cls.OPENAI_BASE_URL:
            config["base_url"] = cls.OPENAI_BASE_URL
        if cls.OPENAI_API_KEY:
            config["api_key"] = cls.OPENAI_API_KEY
        return config

    @classmethod
    def get_search_config(cls) -> Dict[str, Any]:
        """
        获取DuckDuckGo搜索配置

        返回用于配置搜索引擎的参数字典，
        包含搜索结果数量、区域和安全级别。

        返回值：包含搜索配置的字典
        """
        return {
            "max_results": cls.DUCKDUCKGO_MAX_RESULTS,
            "region": cls.DUCKDUCKGO_REGION,
            "safesearch": cls.DUCKDUCKGO_SAFESEARCH,
        }

    @classmethod
    def validate_config(cls) -> bool:
        """
        验证配置是否完整

        检查所有必需的配置项是否存在，
        特别是API密钥等关键配置。

        返回值：配置有效返回True，否则返回False
        """
        if not cls.OPENAI_API_KEY:
            print("⚠️ 警告: 环境变量中未找到 OPENAI_API_KEY")
            print("请在.env文件中设置 OPENAI_API_KEY 或配置兼容网关的密钥")
            return False
        return True

# 初始化配置实例
langgraph_config = LangGraphConfig()

# 在导入时验证配置
if not langgraph_config.validate_config():
    print("❌ 配置验证失败")
    print("请检查您的.env文件并确保设置了 OPENAI_API_KEY")
else:
    print("✅ LangGraph配置加载成功")
