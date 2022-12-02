import logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from app.settings import settings

class MongoClient:
    log: logging.Logger = logging.getLogger(__name__)
    mongo_client = None

    @classmethod
    def get_client(cls):
        """Get MongoDB client"""
        if cls.mongo_client is None:
            cls.log.info(f"Create MongoDB client with URI: {settings.MONGO_URI}")
            cls.mongo_client = MongoClient(settings.MONGO_URI)
        return cls.mongo_client


    @classmethod
    async def close_client(cls):
        """Close MongoDB client"""
        if cls.mongo_client:
            await cls.mongo_client.close()

    
    @classmethod
    async def ping(cls):
        """Ping MongoDB server"""
        try:
            await cls.get_client().server_info()
        except ConnectionFailure:
            cls.log.error("Could not connect to MongoDB")
            return False
        return True

    @classmethod
    def get_db(cls, db_name: str):
        """Get MongoDB database"""
        return cls.get_client()[db_name]