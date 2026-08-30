# Real Estate Unified Search Aggregator

A web application that aggregates real estate listings from major Indian property portals (**MagicBricks**, **99acres**, and **Housing.com**) into a unified search feed.

## 🚀 Features
* **Concurrent Scraping**: Runs parallel async tasks to fetch listings from multiple portals.
* **Akamai/CDN Bypass**: Uses `curl_cffi` to mimic Chrome's TLS fingerprint for reliable scraping on 99acres.
* **Unified API Response**: FastAPI backend normalizes raw data and returns status states for each scraper.
* **Modern UI**: A responsive, clean HTML search dashboard styled with Tailwind CSS.

---

## 🛠 Setup & Installation

### 1. Install Dependencies
Ensure you have Python 3.10+ installed. Install the required libraries:
```bash
pip install fastapi uvicorn httpx beautifulsoup4 curl_cffi
```

### 2. Start the Backend API
Run the FastAPI backend server:
```bash
python app.py
```
The server will start running at `http://localhost:8000`.

### 3. Open the Frontend
Simply open `index.html` in any web browser and search for properties!

---

## 📂 Project Structure
* `app.py`: FastAPI server and scraper logic.
* `index.html`: Tailwind CSS search frontend dashboard.
* `.gitignore`: Git configuration to exclude cache and temp files.
