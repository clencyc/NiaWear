from sqlalchemy import Column, String, Integer
from app.db.database import Base

class ClothingItem(Base):
    __tablename__ = "wardrobe"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    category = Column(String)
    color = Column(String)
    style = Column(String)
    image_url = Column(String)
    season = Column(String, nullable=True)