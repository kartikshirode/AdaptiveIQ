import os
import certifi
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")

client: AsyncIOMotorClient = None  # type: ignore
db = None
questions_collection = None
sessions_collection = None


def get_client():
    global client
    if client is None:
        client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
    return client


def get_db():
    global db
    if db is None:
        db = get_client()["adaptive_engine"]
    return db


def get_questions_collection():
    global questions_collection
    if questions_collection is None:
        questions_collection = get_db()["questions"]
    return questions_collection


def get_sessions_collection():
    global sessions_collection
    if sessions_collection is None:
        sessions_collection = get_db()["sessions"]
    return sessions_collection


async def connect_db():
    pass


async def close_db():
    global client
    if client:
        client.close()
