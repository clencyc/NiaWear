from fastapi import FastAPI, File, UploadFile, HTTPException
import numpy as np
from PIL import Image
import io
from fastapi import APIRouter
from sms import router as sms_router
from AIApi import router as ai_router
from tensorflow.keras.models import load_model

app = FastAPI()
router = APIRouter()

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf'}
model = load_model("path/to/your/model.h5")  # Adjust the path to your model


# file upload endpoint
@router.post("/upload-photo")
async def upload_photo(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    

app.include_router(sms_router, prefix="/sms")
app.include_router(ai_router, prefix="/ai")

@router.get("/test")
async def test_endpoint():
    return {"message": "Router is working"}