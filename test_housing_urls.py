import asyncio
from curl_cffi.requests import AsyncSession

async def test():
    urls = [
        "https://housing.com/in/buy/mumbai/mumbai",
        "https://housing.com/in/buy/mumbai/andheri_west",
        "https://housing.com/in/buy/mumbai/flat-2bhk",
        "https://housing.com/",
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
