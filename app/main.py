from fastapi import FastAPI
from app.routes import user_routes, event_routes, checkin_routes

app = FastAPI(title="QR-Based Event Check-In System")

# Include routers
app.include_router(user_routes.router)
app.include_router(event_routes.router)
app.include_router(checkin_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to QR-Based Event Check-In System"}