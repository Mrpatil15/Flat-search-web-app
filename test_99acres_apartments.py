import asyncio
from curl_cffi.requests import AsyncSession

async def test():
    urls = [
        "https://www.99acres.com/search/property/buy/residential-apartments/mumbai?preference=S&res_com=R&bed_rooms=2",
        "https://www.99acres.com/search/property/buy/residential-apartments/mumbai",
        "https://www.99acres.com/search/property/buy/residential-all/mumbai"
    ]
    async with AsyncSession() as s:
        for url in urls:
            try:
                res = await s.get(url, impersonate="chrome", timeout=10)
                print(f"URL: {url}\nStatus: {res.status_code}, Length: {len(res.text)}\n")
            except Exception as e:
                print(f"URL: {url}\nError: {e}\n")

if __name__ == "__main__":
    asyncio.run(test())
