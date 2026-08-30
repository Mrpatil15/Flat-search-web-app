import asyncio
import httpx
from app import fetch_magicbricks, fetch_99acres, fetch_housing

async def test():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        print("Testing improved MagicBricks...")
        mb = await fetch_magicbricks(client, "2bhk", "Mumbai", "")
        print(f"MagicBricks results: {len(mb)}")
        if mb:
            print("First item:", mb[0])
            
        print("\nTesting improved 99acres (via curl_cffi and JSON state parsing)...")
        acres = await fetch_99acres("2bhk", "Mumbai", "")
        print(f"99acres results: {len(acres)}")
        if acres:
            print("First item:", acres[0])
            
        print("\nTesting Housing.com...")
        housing = await fetch_housing(client, "2bhk", "Mumbai", "")
        print(f"Housing.com status: {housing['status']}")
        print(f"Housing.com results: {len(housing['results'])}")

if __name__ == "__main__":
    asyncio.run(test())
