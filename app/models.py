from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"  # default role is "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM

class EventOut(BaseModel):
    id: str
    title: str
    location: str
    date: str
    time: str

class QRCheckinData(BaseModel):
    email: EmailStr
    event_id: str