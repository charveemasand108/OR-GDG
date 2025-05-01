# app/routes/user_routes.py

from fastapi import APIRouter, HTTPException, Depends
from app.models import UserRegister, UserLogin
from app.auth import hash_password, verify_password, create_access_token
from app.database import users_collection
from bson.objectid import ObjectId

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserRegister):
    # Check if email already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    hashed_pw = hash_password(user.password)
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pw,
        "role": user.role  # 'admin' or 'user'
    }
    users_collection.insert_one(user_data)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    payload = {
        "sub": str(db_user["_id"]),
        "email": db_user["email"],
        "role": db_user["role"]
    }
    token = create_access_token(payload)
    return {"access_token": token, "token_type": "bearer"}
