from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
from typing import Optional


class Database:
    """MongoDB database connection handler."""
    
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None


db = Database()


async def connect_to_mongo():
    """
    Create database connection and initialize indexes.
    Should be called on application startup.
    """
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db.db = db.client[settings.MONGODB_DB_NAME]
    
    # Create indexes
    await create_indexes()
    
    print(f" Connected to MongoDB: {settings.MONGODB_DB_NAME}")


async def close_mongo_connection():
    """
    Close database connection.
    Should be called on application shutdown.
    """
    if db.client:
        db.client.close()
        print(" Closed MongoDB connection")


async def create_indexes():
    """Create database indexes for optimal performance."""
    if db.db is None:
        return
    
    # Users collection indexes
    users_collection = db.db["users"]
    
    # Unique index on phone (primary identifier)
    await users_collection.create_index("phone", unique=True)
    
    # Index on email (optional but for quick lookups)
    await users_collection.create_index("email", sparse=True)
    
    # Index on role for filtering
    await users_collection.create_index("role")
    
    # Index on created_at for sorting
    await users_collection.create_index("created_at")
    
    # OTP collection indexes
    otp_collection = db.db["otps"]
    
    # Compound index on phone and purpose
    await otp_collection.create_index([("phone", 1), ("purpose", 1)])
    
    # TTL index to auto-delete expired OTPs (expires after OTP_EXPIRE_MINUTES)
    await otp_collection.create_index(
        "expires_at",
        expireAfterSeconds=0  # Document expires when expires_at is reached
    )
    
    print(" Database indexes created")


def get_database() -> AsyncIOMotorDatabase:
    """
    Get database instance.
    
    Returns:
        Database instance
        
    Raises:
        RuntimeError: If database is not connected
    """
    if db.db is None:
        raise RuntimeError("Database is not connected")
    return db.db
