from pydantic import BaseModel
from datetime import datetime

class CredentialCreate(BaseModel):
    username: str
    password: str

class CredentialOut(BaseModel):
    id: int
    username: str
    password: str
    ip_address: str | None
    user_agent: str | None
    created_at: datetime
    
    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    username: str
    password: str