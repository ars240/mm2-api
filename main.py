from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

import scraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MM2 Values API",
    description="Real-time MM2 values.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()

@app.on_event("startup")
def startup_event():
    logger.info("Server starting up. Initiating initial scrape...")
    scraper.update_all_data()
    
    scheduler.add_job(
        scraper.update_all_data,
        trigger=IntervalTrigger(minutes=40),
        id='scrape_job',
        name='Scrape MM2Values every 40 mins',
        replace_existing=True
    )
    scheduler.start()
    logger.info("Background scheduler started (40 min interval).")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Server shutting down. Stopping scheduler...")
    scheduler.shutdown()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the MM2 Values API.",
        "endpoints": [
            "/api/all",
            "/api/categories",
            "/api/category/{category_name}"
        ],
        "refresh_interval": "40 minutes"
    }

@app.get("/api/all")
def get_all_items():
    return {"items": scraper.get_all_items()}

@app.get("/api/categories")
def get_categories():
    return {"categories": list(scraper.CATEGORIES.keys())}

@app.get("/api/category/{category_name}")
def get_category_items(category_name: str):
    if category_name not in scraper.CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found.")
    
    items = scraper.get_category(category_name)
    return {"category": category_name, "count": len(items), "items": items}

@app.get("/api/search")
def search_items(q: str):
    query = q.lower()
    results = [item for item in scraper.get_all_items() if query in item["name"].lower()]
    return {"query": q, "count": len(results), "items": results}
