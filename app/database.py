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
_indexes_created = False


def get_client():
    global client
    if client is None:
        client = AsyncIOMotorClient(
            MONGO_URI, 
            tlsCAFile=certifi.where(), 
            serverSelectionTimeoutMS=5000,
            maxPoolSize=10,
            minPoolSize=1
        )
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


async def create_indexes():
    """Create optimized indexes for MongoDB performance."""
    global _indexes_created
    if _indexes_created:
        return
    
    try:
        # Questions collection indexes
        questions_coll = get_questions_collection()
        await questions_coll.create_index("difficulty")  # For sorting by difficulty
        await questions_coll.create_index([("_id", 1)])  # For _id lookups
        await questions_coll.create_index([("topic", 1)])  # For topic filtering
        
        # Sessions collection indexes
        sessions_coll = get_sessions_collection()
        await sessions_coll.create_index([("_id", 1)])  # Primary key is automatic
        await sessions_coll.create_index([("ability_score", 1)])  # For ability sorting
        
        _indexes_created = True
        print("MongoDB indexes created successfully")
    except Exception as e:
        print(f"Error creating indexes: {e}")


async def connect_db():
    """Initialize database connection and create indexes."""
    await create_indexes()


async def close_db():
    global client
    if client:
        client.close()
