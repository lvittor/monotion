import logging

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from app.settings import settings

class MongoDBClient:
    log: logging.Logger = logging.getLogger(__name__)

    @classmethod
    def get_client(cls) -> MongoClient:
        """Get MongoDB client.

        Resources:
            1. https://docs.mongodb.com/manual/reference/connection-string/
            2. https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html

        """
        cls.log.info(f"Creating MongoDB client with URI: {settings.MONGO_URI}")
        client = MongoClient(
            settings.MONGO_URI,
            serverSelectionTimeoutMS=settings.MONGO_SERVER_SELECTION_TIMEOUT_MS,
        )
        return client