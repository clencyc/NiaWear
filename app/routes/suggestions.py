from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.wardrobe import ClothingItem
from app.db.database import get_db
from pydantic import BaseModel
from typing import List, Optional
from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image
import requests

router = APIRouter()

# Initialize CLIP model
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model.eval()

class OutfitResponse(BaseModel):
    items: List[dict]

def compute_image_similarity(image_url1: str, image_url2: str) -> float:
    # Download images
    img1 = Image.open(requests.get(image_url1, stream=True).raw).convert('RGB')
    img2 = Image.open(requests.get(image_url2, stream=True).raw).convert('RGB')
    
    # Process images with CLIP
    inputs = clip_processor(images=[img1, img2], return_tensors="pt", padding=True)
    with torch.no_grad():
        image_features = clip_model.get_image_features(**inputs)
    
    # Compute cosine similarity
    similarity = torch.cosine_similarity(image_features[0], image_features[1], dim=0).item()
    return similarity

@router.get("/suggest/{user_id}", response_model=OutfitResponse)
async def suggest_outfit(user_id: str, style: Optional[str] = None, db: Session = Depends(get_db)):
    items = db.query(ClothingItem).filter(ClothingItem.user_id == user_id).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found for user")

    # Filter by style if specified
    if style:
        items = [item for item in items if item.style.lower() == style.lower()]

    # Group by category
    outfit = {}
    for item in items:
        if item.category not in outfit:
            # Compute similarity with existing outfit items
            is_compatible = True
            for selected_item in outfit.values():
                similarity = compute_image_similarity(item.image_url, selected_item["image_url"])
                if similarity < 0.5:  # Adjust threshold as needed
                    is_compatible = False
                    break
            if is_compatible:
                outfit[item.category] = {
                    "id": item.id,
                    "image_url": item.image_url,
                    "category": item.category,
                    "color": item.color,
                    "style": item.style,
                    "season": item.season
                }

    if not outfit:
        raise HTTPException(status_code=404, detail="No compatible outfit found")

    return {"items": list(outfit.values())}