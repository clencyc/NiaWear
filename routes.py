from fastapi import FastAPI
app = FastAPI()
from sms import router as sms_router
from AIApi import router as ai_router
# Include routers
app.include_router(sms_router, prefix="/sms")
app.include_router(ai_router, prefix="/ai")