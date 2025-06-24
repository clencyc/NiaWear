# IMPORT fastapi
from fastapi import APIRouter, HTTPException, Depends, FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import africastalking
import models  # Import the models module

load_dotenv()

app = FastAPI()

username = os.getenv("AT_USERNAME")
api_key = os.getenv("AT_API_KEY")

africastalking.initialize(username, api_key)
sms = africastalking.SMS

@app.post("/send_sms", response_model=models.SMSResponse)
def sendSms(sms_request: models.SMSRequest):

    welcome_sms = "Welcome to NiaWear, Your Daily Style Guide Personalized fashion tips and trending insights delivered fresh every day"
    try:
        response = sms.send(
            message = welcome_sms, 
            recipients = [sms_request.phone_number]
        )
        if response['SMSMessageData']['Recipients']:
            recipient = response['SMSMessageData']['Recipients'][0]

            if recipient['status'] == 'Success':
                return models.SMSResponse(
                    status="success",
                    message=f"SMS sent successfully to {sms_request.phone_number}",
                    recipients=1,
                    cost=recipient['cost']
                )
            else:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Failed to send SMS: {recipient['status']}"
                )
        else:
            raise HTTPException(status_code=400, detail="No recipients processed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending SMS: {str(e)}")

@app.get("/")
def index():
    return {
        "service": "SMS Service",
        "status": "running",
        "endpoints": [
            "/send_sms",
        ]
    }