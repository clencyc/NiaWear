from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.wardrobe import ClothingItem
from app.db.database import get_db
from typing import List
from pydantic import BaseModel

router = APIRouter()

class ClothingItemCreate(BaseModel):
    user_id: str
    category: str
    color: str
    style: str
    image_url: str
    season: str | None = None

class ClothingItemResponse(ClothingItemCreate):
    id: int

    class Config:
        orm_mode = True

@router.post("/add", response_model=ClothingItemResponse)
async def add_item(item: ClothingItemCreate, db: Session = Depends(get_db)):
    db_item = ClothingItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{user_id}", response_model=List[ClothingItemResponse])
async def get_wardrobe(user_id: str, db: Session = Depends(get_db)):
    items = db.query(ClothingItem).filter(ClothingItem.user_id == user_id).all()
    return items

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ClothingItem).filter(ClothingItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": f"Item with id {item_id} deleted"}