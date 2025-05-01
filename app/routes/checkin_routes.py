from fastapi import APIRouter, HTTPException, Depends, status
from app.models import QRCheckinData
from app.database import registrations_collection, events_collection
from app.auth import decode_access_token
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/checkin", tags=["Check-in"])

def get_current_user(token: str = Depends(decode_access_token)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

@router.post("/scan")
async def scan_qr_code(checkin_data: QRCheckinData, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can perform check-ins")
    
    # Find the registration
    registration = registrations_collection.find_one({
        "event_id": checkin_data.event_id,
        "email": checkin_data.email
    })
    
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    if registration["checked_in"]:
        raise HTTPException(status_code=400, detail="Already checked in")
    
    # Update check-in status
    registrations_collection.update_one(
        {"_id": registration["_id"]},
        {"$set": {
            "checked_in": True,
            "checkin_time": datetime.utcnow(),
            "checked_in_by": current_user["sub"]
        }}
    )
    
    return {"message": "Successfully checked in"}

@router.get("/stats/{event_id}")
async def get_checkin_stats(event_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can view check-in stats")
    
    # Get total registrations
    total_registrations = registrations_collection.count_documents({"event_id": event_id})
    
    # Get checked-in count
    checked_in = registrations_collection.count_documents({
        "event_id": event_id,
        "checked_in": True
    })
    
    # Get event details
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {
        "event_title": event["title"],
        "total_registrations": total_registrations,
        "checked_in": checked_in,
        "pending_checkins": total_registrations - checked_in
    }
