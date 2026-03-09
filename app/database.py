import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")

client: AsyncIOMotorClient = None  # type: ignore
db = None
questions_collection = None
sessions_collection = None


async def connect_db():
    global client, db, questions_collection, sessions_collection
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["adaptive_engine"]
    questions_collection = db["questions"]
    sessions_collection = db["sessions"]


async def close_db():
    global client
    if client:
        client.close()
