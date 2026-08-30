import asyncio
import json
import re
from curl_cffi.requests import AsyncSession
from bs4 import BeautifulSoup

async def debug():
    url = "https://www.99acres.com/property-in-mumbai-ffid"
    async with AsyncSession() as s:
        try:
            res = await s.get(url, impersonate="chrome", timeout=15)
            print("Status:", res.status_code)
            soup = BeautifulSoup(res.text, "html.parser")
            scripts = soup.find_all('script')
            print(f"Found {len(scripts)} scripts")
            for i, script in enumerate(scripts):
                content = script.string or ""
                if "__initialData__" in content:
                    print(f"Script {i} contains __initialData__! Length: {len(content)}")
                    # Let's save a snippet of this script content
                    print(content[:500])
                    # Let's extract and parse the JSON if possible
                    match = re.search(r"window\.__initialData__\s*=\s*(\{.*?\});", content)
                    if match:
                        try:
                            data = json.loads(match.group(1))
                            print("Successfully parsed __initialData__ JSON!")
                            print("Keys in JSON:", list(data.keys()))
                        except Exception as e:
                            print("Error parsing JSON:", e)
                elif "window.__masked__" in content or "window.dataStore" in content:
                    print(f"Script {i} matches dataStore or masked")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    asyncio.run(debug())
