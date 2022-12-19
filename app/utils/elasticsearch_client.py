import logging

from elasticsearch import Elasticsearch
from app.settings import settings

class ElasticsearchClient():
    log: logging.Logger = logging.getLogger(__name__)
    client = None

    @classmethod
    async def get_client(cls):
        """Get Elasticsearch client.
        """
        cls.log.info(f"Creating Elasticsearch client with URI: {settings.ELASTICSEARCH_HOSTS}")
        if not cls.client:
            cls.client = Elasticsearch(
                hosts=settings.ELASTICSEARCH_HOSTS, 
                connection_class=RequestsHttpConnection, 
                max_retries=30,
                retry_on_timeout=True, 
                request_timeout=30
            )
        return cls.client

    @classmethod
    async def close_client(cls) -> None:
        """Close Elasticsearch client."""
        cls.log.info("Closing Elasticsearch client.")
        if cls.client:
            cls.client.close()

    @classmethod
    async def ping(cls) -> bool:
        """Ping Elasticsearch server.
        """
        cls.log.info("Pinging Elasticsearch server.")
        try:
            client = await cls.get_client()
            if not client.ping():
                return ValueError("Connection failed")
        except ValueError as e:
            cls.log.error(f"Elasticsearch server ping failed: {e}")
            return False