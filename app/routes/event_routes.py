from fastapi import APIRouter, HTTPException, Depends, status
from app.models import EventCreate, EventOut
from app.database import events_collection, registrations_collection, users_collection
from app.auth import decode_access_token
from app.utils.qr_email import send_registration_confirmation
from bson import ObjectId
from typing import List
from datetime import datetime

router = APIRouter(prefix="/events", tags=["Events"])

def get_current_user(token: str = Depends(decode_access_token)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

@router.post("/", response_model=EventOut)
async def create_event(event: EventCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create events")
    
    event_data = event.dict()
    event_data["created_by"] = current_user["sub"]
    result = events_collection.insert_one(event_data)
    event_data["id"] = str(result.inserted_id)
    return event_data

@router.get("/", response_model=List[EventOut])
async def get_events():
    events = []
    for event in events_collection.find():
        event["id"] = str(event["_id"])
        events.append(event)
    return events

@router.get("/{event_id}", response_model=EventOut)
async def get_event(event_id: str):
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event["id"] = str(event["_id"])
    return event

@router.post("/{event_id}/register")
async def register_for_event(event_id: str, current_user: dict = Depends(get_current_user)):
    # Check if event exists
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if already registered
    existing_registration = registrations_collection.find_one({
        "event_id": event_id,
        "user_id": current_user["sub"]
    })
    if existing_registration:
        raise HTTPException(status_code=400, detail="Already registered for this event")
    
    # Get user details
    user = users_collection.find_one({"_id": ObjectId(current_user["sub"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create registration
    registration_data = {
        "event_id": event_id,
        "user_id": current_user["sub"],
        "email": current_user["email"],
        "checked_in": False,
        "registration_date": datetime.utcnow()
    }
    registrations_collection.insert_one(registration_data)
    
    # Send confirmation email with QR code
    try:
        send_registration_confirmation(
            email=current_user["email"],
            event_data=event,
            user_data=user
        )
    except Exception as e:
        # Log the error but don't fail the registration
        print(f"Failed to send confirmation email: {str(e)}")
    
    return {"message": "Successfully registered for the event"}
