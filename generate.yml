            stability = "N/A"
            for i, part in enumerate(parts):
                if "Value:" in part:
                    value = parts[i + 1] if i + 1 < len(parts) else "N/A"
                elif "Demand:" in part:
                    demand = parts[i + 1] if i + 1 < len(parts) else "N/A"
                elif "Rarity:" in part:
                    rarity = parts[i + 1] if i + 1 < len(parts) else "N/A"
                elif "Stability:" in part:
                    stability = parts[i + 1] if i + 1 < len(parts) else "N/A"
            img_tag = stack.find("img")
            image = img_tag["src"] if img_tag and img_tag.get("src") else ""
            if image and not image.startswith("http"):
                image = "http://mm2values.com" + image
            items.append({
                "name": name,
                "value": value,
                "demand": demand,
                "rarity": rarity,
                "stability": stability,
                "image": image,
                "category": category_name,
            })
        except Exception as e:
            logger.warning(f"Error parsing item in {category_name}: {e}")
            continue
    logger.info(f"Scraped {len(items)} items from {category_name}")
    return items
def main():
    all_items = []
    for cat_name, cat_suffix in CATEGORIES.items():
        items = scrape_category(cat_name, cat_suffix)
        all_items.extend(items)
    output = {"items": all_items}
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False)
    logger.info(f"Done! Wrote {len(all_items)} items to data.json")
if __name__ == "__main__":
    main()
