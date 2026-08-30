# requirements: fastapi, uvicorn, httpx, beautifulsoup4, curl_cffi
import asyncio
import re
import json
from typing import List, Dict, Any
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession

app = FastAPI(title="Real Estate Unified Aggregator API")

# Enable CORS so the frontend can query the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# --- PORTAL 1: MAGICBRICKS SCRAPER / NORMALIZER ---
async def fetch_magicbricks(client: httpx.AsyncClient, bhk: str, city: str, locality: str) -> List[Dict[str, Any]]:
    results = []
    bhk_digit = "".join(filter(str.isdigit, bhk)) or "2"
    url = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom={bhk_digit}&proptype=Multistorey-Apartment,Builder-Floor-Apartment&cityName={city}"
    
    try:
        res = await client.get(url, headers=HEADERS, timeout=10.0)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.select(".mb-srp__card")[:15]
            for card in cards:
                title_elem = card.select_one(".mb-srp__card--title")
                price_elem = card.select_one(".mb-srp__card__price--amount")
                area_elem = card.select_one(".mb-srp__card__summary--value")
                link_elem = card.select_one("a.mb-srp__card__society--name") or card.select_one("h2 a")

                if title_elem and price_elem:
                    title = title_elem.text.strip()
                    raw_price = price_elem.text.strip()
                    price = f"₹{raw_price}" if "₹" not in raw_price and "Rs" not in raw_price else raw_price
                    # Clean up multiple rupee symbols
                    price = re.sub(r'₹+', '₹', price)
                    
                    area = area_elem.text.strip() if area_elem else "N/A"
                    location = f"{locality}, {city}".strip(", ")
                    
                    # Try to extract the real location from the card title
                    if " in " in title:
                        location_part = title.split(" in ")[-1].strip()
                        if location_part:
                            location = f"{location_part}, {city}"

                    # Filter by locality if provided
                    if locality and locality.lower() not in title.lower() and locality.lower() not in location.lower():
                        continue

                    link = link_elem.get("href", url) if link_elem else url
                    if link and not link.startswith("http"):
                        link = "https://www.magicbricks.com" + link

                    results.append({
                        "portal": "MagicBricks",
                        "badge_color": "bg-red-600",
                        "title": title,
                        "bhk": f"{bhk_digit} BHK",
                        "price": price,
                        "area": area,
                        "location": location,
                        "link": link
                    })
    except Exception as e:
        print(f"MagicBricks Fetch Error: {e}")
    
    return results

# --- PORTAL 2: 99ACRES SCRAPER / NORMALIZER (Using curl_cffi to bypass Akamai) ---
async def fetch_99acres(bhk: str, city: str, locality: str) -> List[Dict[str, Any]]:
    results = []
    bhk_digit = "".join(filter(str.isdigit, bhk)) or "2"
    
    # 99acres uses a stable URL structure based on property-in-{city}-ffid
    url = f"https://www.99acres.com/property-in-{city.lower()}-ffid?bed_rooms={bhk_digit}"
    
    try:
        async with AsyncSession() as s:
            res = await s.get(url, impersonate="chrome", timeout=15)
            if res.status_code == 200:
                # Find the __initialData__ script block containing the preloaded listings state
                match = re.search(r"window\.__initialData__\s*=\s*(\{.*?\});", res.text)
                if match:
                    data = json.loads(match.group(1))
                    properties = data.get('srp', {}).get('pageData', {}).get('properties', [])
                    for prop in properties[:15]:
                        title = prop.get('PROP_HEADING') or prop.get('PROP_NAME') or f"{bhk_digit} BHK Flat"
                        price = prop.get('FORMATTED_PRICE') or prop.get('PRICE') or "Price on Request"
                        
                        # Clean up price format
                        price = f"₹{price}" if "₹" not in str(price) and "Rs" not in str(price) else str(price)
                        price = re.sub(r'₹+', '₹', price)

                        area = f"{prop.get('AREA', 'N/A')} {prop.get('AREA_UNIT', '')}".strip()
                        location = prop.get('LOCALITY') or f"{locality}, {city}".strip(", ")
                        pd_url = prop.get('PROP_DETAILS_URL') or prop.get('PD_URL') or ""
                        if pd_url:
                            if not pd_url.startswith("/"):
                                pd_url = "/" + pd_url
                            link = f"https://www.99acres.com{pd_url}"
                        else:
                            link = url

                        # Filter by locality if provided
                        if locality and locality.lower() not in title.lower() and locality.lower() not in location.lower():
                            continue

                        results.append({
                            "portal": "99acres",
                            "badge_color": "bg-blue-600",
                            "title": title,
                            "bhk": f"{bhk_digit} BHK",
                            "price": price,
                            "area": area,
                            "location": location,
                            "link": link
                        })
            else:
                print(f"99acres returned status code {res.status_code}")
    except Exception as e:
        print(f"99acres Fetch Error: {e}")

    return results

# --- PORTAL 3: HOUSING.COM SCRAPER / NORMALIZER (Graceful fallback) ---
async def fetch_housing(client: httpx.AsyncClient, bhk: str, city: str, locality: str) -> Dict[str, Any]:
    # Returns a dict with "results" and "status" (success or blocked)
    results = []
    bhk_digit = "".join(filter(str.isdigit, bhk)) or "2"
    url = f"https://housing.com/in/buy/{city.lower()}/flat-{bhk_digit}bhk"
    
    try:
        # Try fetching with standard headers first
        res = await client.get(url, headers=HEADERS, timeout=10.0)
        
        # Check if we got challenged/blocked by Akamai
        is_blocked = (res.status_code in [403, 406]) or ("sec-if-cpt-container" in res.text)
        
        if not is_blocked and res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            cards = soup.select("article.css-1y82dva, .card-container")[:10]
            for card in cards:
                title_elem = card.select_one("h2, .css-18z7g97")
                price_elem = card.select_one(".css-180860, .price-text")
                link_elem = card.select_one("a")

                if title_elem:
                    link = link_elem.get("href", "") if link_elem else ""
                    if link and not link.startswith("http"):
                        link = "https://housing.com" + link

                    title = title_elem.text.strip()
                    location = f"{locality}, {city}".strip(", ")
                    
                    if locality and locality.lower() not in title.lower():
                        continue

                    results.append({
                        "portal": "Housing.com",
                        "badge_color": "bg-emerald-600",
                        "title": title,
                        "bhk": f"{bhk_digit} BHK",
                        "price": price_elem.text.strip() if price_elem else "Contact for Price",
                        "area": "Standard layout",
                        "location": location,
                        "link": link or url
                    })
            return {"results": results, "status": "success"}
        else:
            return {"results": [], "status": "blocked_by_akamai"}
    except Exception as e:
        print(f"Housing.com Fetch Error: {e}")
        return {"results": [], "status": f"error: {str(e)}"}

# --- UNIFIED SEARCH ENDPOINT ---
@app.get("/api/search")
async def search_flats(
    bhk: str = Query("2bhk", description="BHK type: 1bhk, 2bhk, 3bhk"),
    city: str = Query("Mumbai", description="City name"),
    locality: str = Query("", description="Optional micro-market/area")
):
    scraper_status = {}
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        # Run scrapers concurrently
        # 1. MagicBricks
        mb_task = fetch_magicbricks(client, bhk, city, locality)
        
        # 2. 99acres (Runs in curl_cffi session separately)
        acres_task = fetch_99acres(bhk, city, locality)
        
        # 3. Housing.com
        housing_task = fetch_housing(client, bhk, city, locality)

        mb_res, acres_res, housing_res_info = await asyncio.gather(mb_task, acres_task, housing_task)

    # Compile scraper statuses
    scraper_status["MagicBricks"] = "success" if mb_res else "empty_or_failed"
    scraper_status["99acres"] = "success" if acres_res else "empty_or_failed"
    scraper_status["Housing.com"] = housing_res_info["status"]

    combined_results = mb_res + acres_res + housing_res_info["results"]
    
    return {
        "status": "success",
        "total_results": len(combined_results),
        "scraper_status": scraper_status,
        "results": combined_results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
