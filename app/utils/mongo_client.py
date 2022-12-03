import logging

from pymongo import MongoClient
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
        cls.log.debug("Get MongoDB client.")
        if not cls.client:
            cls.log.info(f"Creating MongoDB client with URI: {settings.MONGO_URI}")
            cls.client = MongoClient(
                settings.MONGO_URI,
                serverSelectionTimeoutMS=settings.MONGO_SERVER_SELECTION_TIMEOUT_MS,
            )
            # print client server info
            print(f"MongoDB client server info: {cls.client.server_info()}")
        return cls.client

    @classmethod
    async def close_client(cls) -> None:
        """Close MongoDB client.

        Resources:
            1. https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html

        """
        if cls.client:
            cls.log.debug("Closing MongoDB client.")
            await cls.client.close()

    @classmethod
    async def ping(cls) -> bool:
        """Ping MongoDB server.

        Resources:
            1. https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html

        """
        cls.log.debug("Ping MongoDB server.")
        try:
            database = await cls.get_database(settings.MONGO_DB)
            print(database)
            await database.command("ping")
            # # Log database name.
            # cls.log.debug(f"Database name: {database.name}")
            # # check if the database is available.
            # await database.command("")
            return database.name == settings.MONGO_DB
        except ConnectionFailure as e:
            cls.log.error(f"Could not connect to MongoDB, stacktrace={e}")
            return False

    @classmethod
    async def get_database(cls, database_name: str) -> MongoClient:
        """Get MongoDB database.

        Resources:
            1. https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html

        """
        cls.log.debug("Get MongoDB database.")
        client = await cls.get_client()
        return client[database_name]