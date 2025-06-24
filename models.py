from pydantic import BaseModel

class SMSRequest(BaseModel):
    phone_number: str
    
class NiaUser(BaseModel):
    fullname: str
    phone_number: str

class BulkSmsRequest(BaseModel):
    message: str
    recipients: list[NiaUser]

class SMSResponse(BaseModel):
    status: str
    message: str
    recipients: int
    cost: str