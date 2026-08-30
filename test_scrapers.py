import asyncio
import httpx
from app import fetch_magicbricks, fetch_99acres, fetch_housing

async def test():
    async with httpx.AsyncClient(follow_redirects=True) as client:
        print("Testing MagicBricks...")
        mb = await fetch_magicbricks(client, "2bhk", "Mumbai", "Andheri")
        print(f"MagicBricks results: {len(mb)}")
        if mb:
            print("First item:", mb[0])
            
        print("\nTesting 99acres...")
        acres = await fetch_99acres(client, "2bhk", "Mumbai", "Andheri")
        print(f"99acres results: {len(acres)}")
        if acres:
            print("First item:", acres[0])
            
        print("\nTesting Housing.com...")
        housing = await fetch_housing(client, "2bhk", "Mumbai", "Andheri")
        print(f"Housing.com results: {len(housing)}")
        if housing:
            print("First item:", housing[0])

if __name__ == "__main__":
    asyncio.run(test())
