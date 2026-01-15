from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("MONGO_URL not set")

client = AsyncIOMotorClient(MONGO_URL)

database = client["agromarket"]

user_collection = database["users"]
product_collection = database["products"]
cart_collection = database["cart"]
