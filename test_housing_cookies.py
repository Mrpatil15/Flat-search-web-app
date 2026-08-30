import asyncio
from curl_cffi.requests import AsyncSession

async def test():
    async with AsyncSession() as s:
        try:
            # 1. Fetch homepage to get cookies
            res1 = await s.get("https://housing.com/", impersonate="chrome", timeout=15)
            print("Homepage Status:", res1.status_code)
            print("Cookies after homepage:", s.cookies.get_dict())
            
            # 2. Fetch search page
            res2 = await s.get("https://housing.com/in/buy/mumbai/mumbai", impersonate="chrome", timeout=15)
            print("Search Page Status:", res2.status_code)
            print("Search Page Length:", len(res2.text))
            
            # Check if it has Akamai challenge signature
            if "sec-if-cpt-container" in res2.text or "akamai-protected" in res2.text:
                print("Still blocked by Akamai.")
            else:
                print("Success! Not blocked.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    asyncio.run(test())
