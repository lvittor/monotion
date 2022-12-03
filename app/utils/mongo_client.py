import logging

from pymongo import ASCENDING, MongoClient
from pymongo.errors import ConnectionFailure

from app.settings import settings


class MongoDBClient:
    log: logging.Logger = logging.getLogger(__name__)
    client: MongoClient = None

    @classmethod
    async def get_client(cls) -> MongoClient:
        """Get MongoDB client.

        Resources:
            1. https://docs.mongodb.com/manual/reference/connection-string/
            2. https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html

        """
        cls.log.info(f"Creating MongoDB client with URI: {settings.MONGO_URI}")
        if not cls.client:
            cls.client = MongoClient(
                settings.MONGO_URI,
                serverSelectionTimeoutMS=settings.MONGO_SERVER_SELECTION_TIMEOUT_MS,
                authSource="admin",
            )
        return cls.client

    @classmethod
    async def close_client(cls) -> None:
        """Close MongoDB client."""
        cls.log.info("Closing MongoDB client.")
        if cls.client:
            cls.client.close()

    @classmethod
    async def ping(cls) -> bool:
        """Ping MongoDB server.

        Resources:
            1. https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html
        """
        cls.log.info("Pinging MongoDB server.")
        try:
            client = await cls.get_client()
            client.admin.command("ping")
            return True
        except ConnectionFailure as e:
            cls.log.error(f"MongoDB server ping failed: {e}")
            return False

    @classmethod
    async def get_database(cls) -> MongoClient:
        """Get MongoDB database.

        Resources:
            1. https://pymongo.readthedocs.io/en/stable/api/pymongo/database.html

        """
        cls.log.info(f"Getting MongoDB database: {settings.MONGO_DB}")
        client = await cls.get_client()
        database = client[settings.MONGO_DB]
        database.users.create_index([('email', ASCENDING)], unique=True)
        return database
