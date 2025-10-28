"""
配置管理模块

这个模块定义了深度研究助手的配置参数和配置加载逻辑。
支持从环境变量和运行配置中读取参数，环境变量优先级更高。

主要功能：
1. 定义所有可配置的参数
2. 提供配置加载和解析方法
3. 支持多环境配置管理
4. 确保配置的一致性和类型安全
"""

import os
from dataclasses import dataclass, field, fields
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig


@dataclass(kw_only=True)
class Configuration:
    """
    深度研究助手的可配置字段
    
    这个配置类定义了研究助手的所有可配置参数，
    包括研究主题、分析师数量、最大访谈轮次等。
    """
    # 研究主题
    topic: str = "人工智能的发展趋势"
    
    # 分析师数量上限
    max_analysts: int = 3
    
    # 访谈最大轮次
    max_interview_turns: int = 2
    
    # 是否启用人机协同
    enable_human_feedback: bool = True

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """
        从 RunnableConfig 创建 Configuration 实例
        
        这个方法从运行配置中提取配置参数，支持从环境变量和
        配置对象中读取值，环境变量优先级更高。
        
        Args:
            config: 可选的运行配置对象
        
        Returns:
            Configuration: 配置实例
        """
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})

