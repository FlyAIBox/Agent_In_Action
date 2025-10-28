import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from weather_server_mcp import get_daily_forecast


async def main() -> None:
    city = os.getenv("TEST_CITY", "西宁")
    days = int(os.getenv("TEST_DAYS", "3"))
    print(f"Testing get_daily_forecast with city: {city}, days: {days}")
    res = await get_daily_forecast(city, days)
    if isinstance(res, str):
        print(res[:1200])
    else:
        print(str(res)[:1200])


if __name__ == "__main__":
    asyncio.run(main())
