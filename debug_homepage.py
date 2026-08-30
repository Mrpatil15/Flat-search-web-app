import asyncio
from curl_cffi.requests import AsyncSession
from bs4 import BeautifulSoup

async def debug():
    url = "https://www.99acres.com/"
    async with AsyncSession() as s:
        try:
            res = await s.get(url, impersonate="chrome", timeout=15)
            print("99acres Homepage Status:", res.status_code)
            soup = BeautifulSoup(res.text, "html.parser")
            # Find some links containing /buy/ or /search/
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'search' in href or 'buy' in href or 'property-in' in href:
                    links.append((a.text.strip(), href))
            print(f"Found {len(links)} links related to search/buy:")
            for text, href in links[:20]:
                print(f"- {text}: {href}")
        except Exception as e:
            print("Error fetching homepage:", e)

if __name__ == "__main__":
    asyncio.run(debug())
