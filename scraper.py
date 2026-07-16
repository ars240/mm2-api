import requests
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://mm2values.com/"

CATEGORIES = {
    "godly": "?p=godly",
    "chroma": "?p=chroma",
    "ancient": "?p=ancient",
    "unique": "?p=unique",
    "vintage": "?p=vintage",
    "legendary": "?p=legend",
    "rare": "?p=rare",
    "uncommon": "?p=uncommon",
    "common": "?p=common",
    "pets": "?p=pets",
    "misc": "?p=misc",
}

cached_data = {cat: [] for cat in CATEGORIES}

def scrape_category(category_name, url_suffix):
    url = f"{BASE_URL}{url_suffix}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch {category_name}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    stackables = soup.find_all("div", class_="stackable")
    
    for stack in stackables:
        try:
            name_tag = stack.find("b")
            if not name_tag:
                continue
            name = name_tag.text.strip()
            
            text = stack.get_text(separator="|")
            parts = [p.strip() for p in text.split("|") if p.strip()]
            
            value = "N/A"
            demand = "N/A"
            rarity = "N/A"
            stability = "N/A"
            
            for part in parts:
                lower_part = part.lower()
                if lower_part.startswith("value:"):
                    value = part.split(":", 1)[1].strip()
                elif lower_part.startswith("demand:"):
                    d_r = part.split("-")
                    for dr_part in d_r:
                        if "demand:" in dr_part.lower():
                            demand = dr_part.split(":", 1)[1].strip()
                        elif "rarity:" in dr_part.lower():
                            rarity = dr_part.split(":", 1)[1].strip()
                elif lower_part.startswith("stability:"):
                    stability = part.split(":", 1)[1].strip()
            
            img_url = ""
            img_tag = stack.find("img")
            if img_tag and img_tag.has_attr("src"):
                img_url = img_tag["src"]
                if not img_url.startswith("http"):
                    img_url = f"{BASE_URL}{img_url}"
            
            items.append({
                "name": name,
                "value": value,
                "demand": demand,
                "rarity": rarity,
                "stability": stability,
                "image": img_url,
                "category": category_name
            })
        except Exception as e:
            logger.warning(f"Error parsing an item in {category_name}: {e}")
            continue

    logger.info(f"Scraped {len(items)} items for {category_name}.")
    return items

def update_all_data():
    logger.info("Starting scheduled scrape of all MM2 Values categories...")
    for cat, suffix in CATEGORIES.items():
        items = scrape_category(cat, suffix)
        if items:
            cached_data[cat] = items
        time.sleep(1)
    logger.info("Completed scraping all categories.")

def get_all_items():
    all_items = []
    for items in cached_data.values():
        all_items.extend(items)
    return all_items

def get_category(cat_name):
    return cached_data.get(cat_name, [])

if __name__ == "__main__":
    update_all_data()
    print(f"Total items scraped: {len(get_all_items())}")
