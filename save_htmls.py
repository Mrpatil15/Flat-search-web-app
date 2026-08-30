import asyncio
from curl_cffi.requests import AsyncSession

async def save_htmls():
    async with AsyncSession() as s:
        # 99acres
        try:
            res = await s.get("https://www.99acres.com/search/property/buy/mumbai?preference=S&res_com=R&bed_rooms=2", impersonate="chrome")
            with open("99acres_res.html", "w", encoding="utf-8") as f:
                f.write(res.text)
            print("Saved 99acres status:", res.status_code)
        except Exception as e:
            print("99acres error:", e)

        # Housing.com
        try:
            res = await s.get("https://housing.com/in/buy/searches?city=Mumbai&num_bedrooms=2", impersonate="chrome")
            with open("housing_res.html", "w", encoding="utf-8") as f:
                f.write(res.text)
            print("Saved Housing.com status:", res.status_code)
        except Exception as e:
            print("Housing.com error:", e)

if __name__ == "__main__":
    asyncio.run(save_htmls())
