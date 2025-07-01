from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.models.wardrobe import ClothingItem
from app.db.database import get_db
from app.ml.model import load_model, predict_image
import os
from pydantic import BaseModel

router = APIRouter()

# Initialize model once
model = load_model()

class ClothingItemCreate(BaseModel):
    user_id: str
    color: str
    style: str
    season: str | None = None

class ClothingItemResponse(BaseModel):
    id: int
    user_id: str
    category: str
    color: str
    style: str
    image_url: str
    season: str | None

    class Config:
        orm_mode = True

@router.post("/classify", response_model=ClothingItemResponse)
async def classify_and_add_item(
    user_id: str,
    color: str,
    style: str,
    season: str | None = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate file
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be an image")

    # Save image temporarily
    image_path = f"Uploads/{file.filename}"
    with open(image_path, "wb") as f:
        f.write(file.file.read())

    try:
        # Predict category
        category = predict_image(image_path, model)

        # Save to Uploads directory (or use Cloudinary)
        image_url = f"/Uploads/{file.filename}"  # Update with Cloudinary URL if used

        # Save to database
        db_item = ClothingItem(
            user_id=user_id,
            category=category,
            color=color,
            style=style,
            image_url=image_url,
            season=season
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item
    finally:
        # Clean up temporary file
        if os.path.exists(image_path):
            os.remove(image_path)