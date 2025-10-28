"""
应用程序配置设置

这个模块定义了整个旅行规划系统的配置参数，包括：
- 应用程序基本信息
- 默认设置和限制
- 结果数量限制
- 缓存和文件设置
- 显示和成本估算参数

适用于大模型技术初级用户：
这个模块展示了如何组织应用程序的配置，
通过集中管理参数来提高系统的可维护性。
"""

# 应用程序基本设置
APP_NAME = "AI旅行规划助手"  # 应用程序名称
VERSION = "1.0.0"                    # 版本号

# 默认设置
DEFAULT_CURRENCY = "CNY"             # 默认货币：人民币
DEFAULT_BUDGET_RANGE = "中等预算"     # 默认预算范围
DEFAULT_TRIP_DURATION = 7            # 默认旅行天数

# 限制和约束条件
MAX_TRIP_DURATION = 90               # 最大旅行天数
MIN_TRIP_DURATION = 1                # 最小旅行天数
MAX_GROUP_SIZE = 20                  # 最大团队人数
MIN_GROUP_SIZE = 1                   # 最小团队人数

# 结果数量限制
# 这些限制确保系统性能和用户体验的平衡
MAX_ATTRACTIONS = 10                 # 最大景点推荐数量
MAX_RESTAURANTS = 8                  # 最大餐厅推荐数量
MAX_ACTIVITIES = 6                   # 最大活动推荐数量
MAX_HOTELS = 8                       # 最大酒店推荐数量

# 缓存设置
# 缓存可以提高系统性能，减少重复的API调用
CACHE_DURATION_HOURS = 1             # 缓存持续时间（小时）
MAX_CACHE_SIZE = 100                 # 最大缓存大小

# 文件设置
OUTPUT_DIRECTORY = "旅行计划"         # 输出目录名称
MAX_FILE_SIZE_MB = 10                # 最大文件大小（MB）

# 显示设置
MAX_DISPLAY_ITEMS = 5                # 最大显示项目数量
TRUNCATE_DESCRIPTION_LENGTH = 100    # 描述截断长度

# 成本估算设置
EMERGENCY_FUND_PERCENTAGE = 0.15     # 应急资金百分比（15%缓冲）
TAX_AND_FEES_PERCENTAGE = 0.08       # 税费百分比（8%用于税费）

# 天气预报设置
MAX_FORECAST_DAYS = 16               # 最大预报天数
WEATHER_UPDATE_INTERVAL_HOURS = 6    # 天气更新间隔（小时）

# 创建应用配置对象供导入使用
class AppConfig:
    """
    应用程序配置类

    这个类封装了应用程序的主要配置参数，
    提供统一的配置访问接口。

    适用于大模型技术初级用户：
    这种设计模式将配置集中管理，
    使得修改配置变得简单和安全。
    """
    DEFAULT_CURRENCY = DEFAULT_CURRENCY           # 默认货币
    DEFAULT_BUDGET_RANGE = DEFAULT_BUDGET_RANGE   # 默认预算范围
    MAX_ATTRACTIONS = MAX_ATTRACTIONS             # 最大景点数量
    MAX_RESTAURANTS = MAX_RESTAURANTS             # 最大餐厅数量
    MAX_ACTIVITIES = MAX_ACTIVITIES               # 最大活动数量
    MAX_HOTELS = MAX_HOTELS                       # 最大酒店数量

# 全局实例供导入使用
app_config = AppConfig()