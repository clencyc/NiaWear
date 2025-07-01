from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import wardrobe, classifier, suggestions
from dotenv import load_dotenv
from app.db.database import get_db
from sqlalchemy.orm import Session

load_dotenv()

app = FastAPI(title="NiaWear Style API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "https://niawear-style.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wardrobe.router, prefix="/wardrobe")
app.include_router(classifier.router, prefix="/classifier")
app.include_router(suggestions.router, prefix="/suggestions")

@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "NiaWear Style API"}

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")