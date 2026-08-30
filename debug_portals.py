import asyncio
import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

async def debug_99acres():
    url = "https://www.99acres.com/search/property/buy/mumbai?preference=S&res_com=R&bed_rooms=2"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            res = await client.get(url, headers=HEADERS, timeout=10.0)
            print("99acres Status:", res.status_code)
            print("99acres HTML Length:", len(res.text))
            soup = BeautifulSoup(res.text, "html.parser")
            print("99acres title tags found:", len(soup.select(".tupleNew__propType, .tuple__propType")))
            print("99acres body snippet:", res.text[:500])
        except Exception as e:
            print("99acres error:", e)

async def debug_housing():
    url = "https://housing.com/in/buy/searches?city=Mumbai&num_bedrooms=2"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            res = await client.get(url, headers=HEADERS, timeout=10.0)
            print("Housing.com Status:", res.status_code)
            print("Housing.com HTML Length:", len(res.text))
            soup = BeautifulSoup(res.text, "html.parser")
            print("Housing.com card tags found:", len(soup.select("article.css-1y82dva, .card-container")))
            print("Housing.com body snippet:", res.text[:500])
        except Exception as e:
            print("Housing.com error:", e)

if __name__ == "__main__":
    asyncio.run(debug_99acres())
    asyncio.run(debug_housing())
