import asyncio
import json
import re
from curl_cffi.requests import AsyncSession
from bs4 import BeautifulSoup

async def debug():
    url = "https://www.99acres.com/property-in-mumbai-ffid?bed_rooms=2"
    async with AsyncSession() as s:
        try:
            res = await s.get(url, impersonate="chrome", timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")
            for script in soup.find_all('script'):
                content = script.string or ""
                if "__initialData__" in content:
                    match = re.search(r"window\.__initialData__\s*=\s*(\{.*?\});", content)
                    if match:
                        data = json.loads(match.group(1))
                        properties = data.get('srp', {}).get('pageData', {}).get('properties', [])
                        if properties:
                            print("Number of properties:", len(properties))
                            print("First property JSON keys:")
                            print(list(properties[0].keys()))
                            print("\nFirst property sample data:")
                            # Print some key info
                            prop = properties[0]
                            for k in ['PROP_NAME', 'PRICE', 'AREA', 'UNIT_NAME', 'BUILDING_NAME', 'ADDRESS', 'CITY_NAME', 'LocalityName', 'OUR_URL', 'URL']:
                                if k in prop:
                                    print(f"  {k}: {prop[k]}")
                                else:
                                    # Search for key case-insensitive
                                    for pk in prop.keys():
                                        if pk.upper() == k:
                                            print(f"  {pk} (matched {k}): {prop[pk]}")
                            # Let's print the entire dictionary of the first property
                            print("\nFull first property dict:")
                            print(json.dumps(prop, indent=2)[:2000])
                        else:
                            print("No properties list found in pageData")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    asyncio.run(debug())
