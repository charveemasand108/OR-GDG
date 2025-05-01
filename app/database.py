from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

# Database and collections
db = client.qr_checkin
users_collection = db.users
events_collection = db["events"]
registrations_collection = db["registrations"]