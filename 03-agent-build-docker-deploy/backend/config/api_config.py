"""
外部服务API配置

这个模块管理所有外部 API 服务的配置，包括：
- 和风天气 (QWeather)：天气数据与灾害预警

适用于大模型技术初级用户：
这个模块展示了如何通过环境变量安全地管理国内可访问的 API，
在不同部署环境中灵活替换服务提供商。
"""

import os
from typing import Optional

# 和风天气 (QWeather) API 配置
QWEATHER_API_KEY: Optional[str] = os.getenv("QWEATHER_API_KEY")
QWEATHER_API_BASE: str = os.getenv("QWEATHER_API_BASE")

def get_api_status() -> dict:
    """
    检查哪些 API 具有有效的密钥

    返回：包含天气、地点、汇率服务可用性的字典
    """
    return {
        "weather": bool(QWEATHER_API_KEY),
    }

class APIConfig:
    """
    API 配置类

    将外部服务的配置集中管理，便于其他模块导入使用。
    """

    QWEATHER_API_KEY = QWEATHER_API_KEY
    QWEATHER_API_BASE = QWEATHER_API_BASE

# 全局实例供导入使用
api_config = APIConfig()