import asyncio
from curl_cffi.requests import AsyncSession
from bs4 import BeautifulSoup

async def debug_99acres():
    url = "https://www.99acres.com/search/property/buy/mumbai?preference=S&res_com=R&bed_rooms=2"
    async with AsyncSession() as s:
        try:
            res = await s.get(url, impersonate="chrome", timeout=15)
            print("99acres (curl_cffi) Status:", res.status_code)
            print("99acres (curl_cffi) HTML Length:", len(res.text))
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.select(".tupleNew__tupleWrap, .tuple__tupleWrap")
            print("99acres (curl_cffi) cards found:", len(cards))
        except Exception as e:
            print("99acres error:", e)

async def debug_housing():
    url = "https://housing.com/in/buy/searches?city=Mumbai&num_bedrooms=2"
    async with AsyncSession() as s:
        try:
            res = await s.get(url, impersonate="chrome", timeout=15)
            print("Housing.com (curl_cffi) Status:", res.status_code)
            print("Housing.com (curl_cffi) HTML Length:", len(res.text))
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.select("article.css-1y82dva, .card-container")
            print("Housing.com (curl_cffi) cards found:", len(cards))
            # Also let's print a card details if found
            if cards:
                print("First card title:", cards[0].text[:100])
        except Exception as e:
            print("Housing.com error:", e)

if __name__ == "__main__":
    asyncio.run(debug_99acres())
    asyncio.run(debug_housing())
