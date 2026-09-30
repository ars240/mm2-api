import scraper
import json

scraper.update_all_data()

all_items = []
for cat, items in scraper.cached_data.items():
    all_items.extend(items)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump({"items": all_items}, f, ensure_ascii=False)

print(f"Done! Wrote {len(all_items)} items to data.json")
