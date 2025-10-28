"""AI 旅行规划智能体 - 数据模型定义模块

此文件集中定义了旅行规划过程中所需的核心实体模型，涵盖天气、景点、酒店、交通、每日行程、整体行程总结等。
各数据结构为 `dataclass`，便于在多智能体协作、业务逻辑处理和结果渲染过程中快速创建、序列化与调试。
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import date, datetime

@dataclass
class Weather:
    """单日天气信息实体，供行程安排与建议参考。"""
    temperature: float  # 摄氏温度
    description: str  # 天气概况描述，如“阴转多云”
    humidity: int  # 相对湿度，百分比
    wind_speed: float  # 风速，单位 km/h
    feels_like: float  # 体感温度，摄氏度
    date: str  # 日期字符串，格式 YYYY-MM-DD
    
    def __str__(self) -> str:
        """将天气信息格式化为易读字符串，便于日志或界面展示。"""
        return f"{self.description}, {self.temperature}°C (feels like {self.feels_like}°C)"

@dataclass  
class Attraction:
    """景点/餐厅/活动等 POI（Point of Interest）实体。"""
    name: str  # 名称
    type: str  # 分类：'attraction'、'restaurant'、'activity' 等
    rating: float  # 评分，1-5 星
    price_level: int  # 价格级别，0-4（参考 Google Places 规范）
    address: str  # 地址信息
    description: str  # 简要描述，用于提示/介绍
    estimated_cost: float  # 预估花费，单位 USD
    duration: int  # 预计停留时长，单位小时
    
    def __str__(self) -> str:
        """便捷输出，显示名称、评分与费用概览。"""
        return f"{self.name} ({self.rating}⭐) - ${self.estimated_cost}"

@dataclass
class Hotel:
    """酒店住宿选项实体，包含价格、评分与设施等核心信息。"""
    name: str  # 酒店名称
    rating: float  # 评分，1-5 星
    price_per_night: float  # 每晚价格，单位 USD
    address: str  # 地址
    amenities: List[str]  # 设施列表，如 WiFi、早餐、泳池等
    
    def calculate_total_cost(self, nights: int) -> float:
        """根据入住晚数计算总费用。"""
        return self.price_per_night * nights
    
    def __str__(self) -> str:
        """返回酒店的主要信息（名称、评分、价格）。"""
        return f"{self.name} ({self.rating}⭐) - ${self.price_per_night}/night"

@dataclass
class Transportation:
    """交通方式实体，用于描述行程中各段位移手段及成本。"""
    mode: str  # 交通方式（步行/公共交通/出租车/Uber 等）
    estimated_cost: float  # 预估费用，单位 USD
    duration: int  # 预计耗时，单位分钟
    
    def __str__(self) -> str:
        """返回交通方式的简洁描述。"""
        return f"{self.mode} - ${self.estimated_cost} ({self.duration} min)"

@dataclass
class DayPlan:
    """单日行程计划实体，汇总当天的天气、活动与交通安排。"""
    day: int  # 天数编号（第几天）
    date: str  # 日期字符串，YYYY-MM-DD
    weather: Weather  # 当天天气信息
    attractions: List[Attraction] = None  # 计划景点列表
    restaurants: List[Attraction] = None  # 餐饮安排列表
    activities: List[Attraction] = None  # 其他活动列表
    transportation: List[Transportation] = None  # 交通安排
    daily_cost: float = 0.0  # 当日预估总费用
   
    def __post_init__(self):
        """初始化列表属性，防止使用默认可变对象导致引用共享。"""
        if self.attractions is None:
            self.attractions = []
        if self.restaurants is None:
            self.restaurants = []
        if self.activities is None:
            self.activities = []
        if self.transportation is None:
            self.transportation = []
    
    def get_total_activities(self) -> int:
        """获取当天所有活动数量（景点+餐饮+其他活动）。"""
        return len(self.attractions) + len(self.restaurants) + len(self.activities)
    
    def __str__(self) -> str:
        """简要描述当天安排概要。"""
        return f"Day {self.day} ({self.date}) - {self.get_total_activities()} activities, ${self.daily_cost}"

@dataclass
class TripSummary:
    """完整行程总结实体，包含从时间、费用到亮点推荐等综合信息。"""
    destination: str  # 目的地
    start_date: date  # 出发日期
    end_date: date  # 结束日期
    total_days: int  # 总天数
    total_cost: float  # 总费用（原始币种）
    daily_budget: float  # 每日预算
    currency: str  # 原始币种
    converted_total: float  # 换算至目标币种后的总费用
    itinerary: List[DayPlan]  # 按天行程列表
    hotels: List[Hotel]  # 推荐酒店列表
    
    # Additional summary data (added by TripSummaryGenerator)
    trip_overview: Dict[str, Any] = None  # 行程概览
    weather_summary: Dict[str, Any] = None  # 天气总结
    accommodation_summary: Dict[str, Any] = None  # 住宿总结
    expense_summary: Dict[str, Any] = None  # 费用总结
    itinerary_highlights: Dict[str, Any] = None  # 行程亮点
    recommendations: Dict[str, Any] = None  # 个性化建议
    travel_tips: List[str] = None  # 旅行贴士列表
    
    def __post_init__(self):
        """初始化各总结字段，避免 None 导致后续赋值报错。"""
        if self.trip_overview is None:
            self.trip_overview = {}
        if self.weather_summary is None:
            self.weather_summary = {}
        if self.accommodation_summary is None:
            self.accommodation_summary = {}
        if self.expense_summary is None:
            self.expense_summary = {}
        if self.itinerary_highlights is None:
            self.itinerary_highlights = {}
        if self.recommendations is None:
            self.recommendations = {}
        if self.travel_tips is None:
            self.travel_tips = []
    
    def get_cost_per_person(self, group_size: int) -> float:
        """计算人均费用；若 group_size <= 0，则返回总费用。"""
        return self.converted_total / group_size if group_size > 0 else self.converted_total
    
    def get_average_daily_cost(self) -> float:
        """计算平均每天花费。"""
        return self.converted_total / self.total_days if self.total_days > 0 else 0.0
    
    def __str__(self) -> str:
        """返回整体行程概要字符串。"""
        return f"Trip to {self.destination} ({self.total_days} days) - {self.currency} {self.converted_total:.2f}"

# Utility functions for model creation
def create_mock_weather(temperature: float = 22.0, description: str = "Partly Cloudy", date_str: str = None) -> Weather:
    """生成测试用 Weather 对象，便于单元测试或示例演示。"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    return Weather(
        temperature=temperature,
        description=description,
        humidity=65,
        wind_speed=10.0,
        feels_like=temperature + 2,
        date=date_str
    )

def create_mock_attraction(name: str = "Sample Attraction", attraction_type: str = "attraction") -> Attraction:
    """生成测试用 Attraction 对象。"""
    return Attraction(
        name=name,
        type=attraction_type,
        rating=4.2,
        price_level=2,
        address="Sample Address",
        description="Sample description",
        estimated_cost=25.0,
        duration=2
    )

def create_mock_hotel(name: str = "Sample Hotel") -> Hotel:
    """生成测试用 Hotel 对象。"""
    return Hotel(
        name=name,
        rating=4.0,
        price_per_night=100.0,
        address="Sample Hotel Address",
        amenities=["WiFi", "Breakfast", "Pool"]
    )
