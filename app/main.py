import logging

from fastapi import FastAPI

from app.exceptions.http import HTTPException, http_exception_handler
from app.router import root_api_router
from app.settings import settings
from app.utils.aiohttp_client import AiohttpClient
from app.utils.mongo_client import MongoDBClient
from app.utils.elasticsearch_client import ElasticsearchClient


async def on_startup():
    """Define FastAPI startup event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#startup-event

    """
    log.debug("Execute FastAPI startup event handler.")

    await MongoDBClient.get_client()
    await ElasticsearchClient.start_indexes()
    AiohttpClient.get_aiohttp_client()
   


async def on_shutdown():
    """Define FastAPI shutdown event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event

    """
    log.debug("Execute FastAPI shutdown event handler.")

    await MongoDBClient.close_client()
    await AiohttpClient.close_aiohttp_client()
    await ElasticsearchClient.close_client()
    
app = FastAPI(debug=settings.DEBUG, on_startup=[on_startup], on_shutdown=[on_shutdown], title="Monotion", description="A Notion-like block management system.")
log = logging.getLogger(__name__)

app.include_router(root_api_router)
app.add_exception_handler(HTTPException, http_exception_handler)
