import motor.motor_asyncio
import certifi
from app.config import settings

_client = None
_database = None


def get_client():
    global _client
    if _client is None:
        _client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.DATABASE_URL,
            tlsCAFile=certifi.where()
        )
    return _client


def get_database():
    global _database
    if _database is None:
        client = get_client()
        _database = client.get_database()
    return _database


@property
def users_collection():
    return get_database().get_collection("users")


@property
def zones_collection():
    return get_database().get_collection("zones")


database = get_database()
users_collection = database.get_collection("users")
zones_collection = database.get_collection("zones")


async def get_db():
    return get_database()


async def create_indexes():
    db = get_database()
    
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)
    await db.zones.create_index("name", unique=True)
    await db.zones.create_index("id", unique=True)


async def close_db_connection():
    global _client
    if _client:
        _client.close()
        _client = None
