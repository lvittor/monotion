import logging

from elasticsearch import Elasticsearch
from app.settings import settings
from app.utils.mongo_client import MongoDBClient
from app.models import Block, BlockType

import json
from bson import json_util

class ElasticsearchClient():
    log: logging.Logger = logging.getLogger(__name__)
    client = None

    @classmethod
    async def get_client(cls):
        """Get Elasticsearch client."""
        print(f"Creating Elasticsearch client with URI: {settings.ELASTICSEARCH_HOSTS}")
        if not cls.client:
            cls.client = Elasticsearch(
                hosts=settings.ELASTICSEARCH_HOSTS, 
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
                raise ValueError("Connection failed") 
            return True
        except ValueError as e:
            cls.log.error(f"Elasticsearch server ping failed: {e}")
            return False

    @classmethod
    def to_json(cls, _dict):
        return json.loads(json_util.dumps(_dict))

    @classmethod
    async def start_indexes(cls):
        db = await MongoDBClient.get_database()
        es = await cls.get_client()
        blocks = list(db.blocks.find({}))

        for _ in blocks:
            block = Block(**_)
            if block.type == BlockType.PAGE.value:
                dict_index = {"id": str(_["_id"]), "title": block.properties['title'], "is_public": block.is_public, "page_owner": str(_["page_owner"])}
                es_response = es.index(index="title-index", document=ElasticsearchClient.to_json(dict_index))
            else:
                dict_index = {"id": str(_["_id"]), "type": block.type, "properties": block.properties, "is_public": block.is_public, "creator": str(_["page_owner"])}
                es_response = es.index(index="content-index", document=ElasticsearchClient.to_json(dict_index))

        users = list(db.users.find({}))
        for _ in users:
            es_dict = {
                'id': str(_["_id"]),
                'username': _['username'],
                'email': _['email'],
            }
            es.index(index="user-index", document=ElasticsearchClient.to_json(es_dict))



