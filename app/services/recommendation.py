from typing import List, Optional
from app.models.wardrobe import ClothingItem
import random

def suggest_outfit(wardrobe: List[ClothingItem], weather: dict, occasion: str, description: Optional[str] = None) -> List[ClothingItem]:
    temperature = weather["temperature"]
    condition = weather["condition"]

    outfit_categories = {
        "casual": ["shirt", "pants", "shoes"],
        "formal": ["shirt", "suit", "shoes"],
        "business": ["blazer", "shirt", "pants"],
        "sport": ["shirt", "shorts", "sneakers"],
    }
    target_categories = outfit_categories.get(occasion.lower(), ["shirt", "pants", "shoes"])

    filtered_items = []
    for item in wardrobe:
        if temperature < 10 and item.season == "winter":
            filtered_items.append(item)
        elif temperature > 20 and item.season == "summer":
            filtered_items.append(item)
        elif condition == "Rain" and item.category in ["jacket", "coat"]:
            filtered_items.append(item)
        elif occasion.lower() == item.style.lower() or occasion.lower() == "random":
            filtered_items.append(item)

    if description:
        filtered_items = [
            item for item in filtered_items
            if any(keyword.lower() in description.lower() for keyword in [item.category, item.color, item.style])
        ]

    items_by_category = {cat: [] for cat in target_categories}
    for item in filtered_items:
        if item.category in target_categories:
            items_by_category[item.category].append(item)

    outfit = []
    for cat in target_categories:
        if items_by_category[cat]:
            outfit.append(random.choice(items_by_category[cat]))

    if len(outfit) < len(target_categories) and occasion.lower() == "random":
        remaining = [item for item in filtered_items if item not in outfit]
        random.shuffle(remaining)
        outfit.extend(remaining[:len(target_categories) - len(outfit)])

    return outfit[:3]