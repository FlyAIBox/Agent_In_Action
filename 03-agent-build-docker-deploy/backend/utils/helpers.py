"""
实用工具函数模块

这个模块包含了整个旅行规划系统中使用的通用工具函数，包括：
- 数据验证和格式化
- 日期和时间处理
- 文件操作和安全处理
- 货币格式化和计算
- 文本处理和显示

适用于大模型技术初级用户：
这个模块展示了如何编写可重用的工具函数，
提高代码的模块化和可维护性。
"""

from datetime import datetime, date
from typing import Dict, Any, Tuple, List
import re

def validate_email(email: str) -> bool:
    """
    验证邮箱格式

    使用正则表达式验证邮箱地址的格式是否正确。

    参数：
    - email: 要验证的邮箱地址字符串

    返回：如果格式正确返回True，否则返回False

    适用于大模型技术初级用户：
    正则表达式是一种强大的文本匹配工具，
    这里用来确保用户输入的邮箱格式正确。
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_currency(amount: float, currency: str = "CNY") -> str:
    """
    格式化货币金额显示

    将数字金额格式化为带货币符号的字符串，
    支持多种国际货币。

    参数：
    - amount: 金额数值
    - currency: 货币代码（默认：CNY人民币）

    返回：格式化的货币字符串

    适用于大模型技术初级用户：
    这个函数展示了如何处理国际化的货币显示，
    使用字典映射货币代码到符号。
    """
    symbols = {
        'CNY': '¥',   # 人民币
        'USD': '$',   # 美元
        'EUR': '€',   # 欧元
        'GBP': '£',   # 英镑
        'INR': '₹',   # 印度卢比
        'JPY': '¥',   # 日元
        'CAD': 'C$',  # 加拿大元
        'AUD': 'A$'   # 澳大利亚元
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"

def calculate_days_between_dates(start_date: date, end_date: date) -> int:
    """
    计算两个日期之间的天数

    计算旅行开始日期和结束日期之间的天数差。

    参数：
    - start_date: 开始日期
    - end_date: 结束日期

    返回：天数差（整数）
    """
    return (end_date - start_date).days

def sanitize_filename(filename: str) -> str:
    """
    清理文件名中的无效字符

    移除或替换文件名中不允许的字符，
    确保文件名在不同操作系统中都有效。

    参数：
    - filename: 原始文件名

    返回：清理后的安全文件名

    适用于大模型技术初级用户：
    这个函数展示了如何处理跨平台的文件名兼容性问题。
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def parse_date_string(date_str: str) -> date:
    """
    解析日期字符串

    将YYYY-MM-DD格式的字符串转换为日期对象。

    参数：
    - date_str: 日期字符串（格式：YYYY-MM-DD）

    返回：日期对象
    """
    return datetime.strptime(date_str, '%Y-%m-%d').date()

def get_season_from_date(travel_date: date) -> str:
    """
    根据旅行日期确定季节

    基于月份判断旅行日期所属的季节（北半球）。

    参数：
    - travel_date: 旅行日期

    返回：季节名称（中文）

    适用于大模型技术初级用户：
    这个函数展示了如何根据业务逻辑进行条件判断。
    """
    month = travel_date.month
    if month in [12, 1, 2]:
        return "冬季"
    elif month in [3, 4, 5]:
        return "春季"
    elif month in [6, 7, 8]:
        return "夏季"
    else:
        return "秋季"

def calculate_percentage(part: float, total: float) -> float:
    """
    计算百分比（带错误处理）

    安全地计算部分占总数的百分比，
    避免除零错误。

    参数：
    - part: 部分数值
    - total: 总数值

    返回：百分比（保留1位小数）

    适用于大模型技术初级用户：
    这个函数展示了如何进行安全的数学计算，
    包含错误处理和边界条件检查。
    """
    if total == 0:
        return 0.0
    return round((part / total) * 100, 1)

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    截断文本到指定长度

    如果文本超过最大长度，则截断并添加省略号。

    参数：
    - text: 原始文本
    - max_length: 最大长度（默认100字符）

    返回：截断后的文本

    适用于大模型技术初级用户：
    这个函数展示了如何处理用户界面中的文本显示，
    确保界面整洁和一致性。
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def group_items_by_key(items: List[Dict], key: str) -> Dict[str, List[Dict]]:
    """
    按指定键对字典列表进行分组

    将字典列表按某个键的值进行分组，
    便于数据的组织和处理。

    参数：
    - items: 字典列表
    - key: 分组依据的键名

    返回：分组后的字典

    适用于大模型技术初级用户：
    这个函数展示了数据结构的转换和组织技巧，
    是数据处理中的常用模式。
    """
    grouped = {}
    for item in items:
        group_key = item.get(key, '未知')
        if group_key not in grouped:
            grouped[group_key] = []
        grouped[group_key].append(item)
    return grouped

def display_header():
    """
    显示应用程序标题

    在控制台输出格式化的应用程序标题和功能介绍。

    适用于大模型技术初级用户：
    这个函数展示了如何创建用户友好的命令行界面。
    """
    print("\n" + "="*80)
    print("🤖 AI旅行助手与费用规划师")
    print("="*80)
    print("实时天气 • 热门景点 • 成本分析 • 完整行程")
    print("="*80)

def save_to_file(content: str, filename: str) -> bool:
    """
    保存内容到文件（带错误处理）

    安全地将文本内容保存到文件，
    包含完整的错误处理机制。

    参数：
    - content: 要保存的内容
    - filename: 文件名

    返回：保存成功返回True，失败返回False

    适用于大模型技术初级用户：
    这个函数展示了文件操作的最佳实践，
    包括异常处理和资源管理。
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"保存文件时出错: {e}")
        return False
