import logging

from fastapi import FastAPI

from app.exceptions.http import HTTPException, http_exception_handler
from app.router import root_api_router
from app.settings import settings
from app.utils.aiohttp_client import AiohttpClient
from pymongo import MongoClient


async def on_startup():
    """Define FastAPI startup event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#startup-event

    """
    log.debug("Execute FastAPI startup event handler.")
    print(settings.MONGO_URI)
    app.mongodb_client = MongoClient(settings.MONGO_URI)
    app.database = app.mongodb_client[settings.MONGO_DB]
    # ping MongoDB
    app.database["mongodb"].insert_one({"ping": "pong"})
    AiohttpClient.get_aiohttp_client()


async def on_shutdown():
    """Define FastAPI shutdown event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event

    """
    log.debug("Execute FastAPI shutdown event handler.")

    app.mongodb_client.close()
    await AiohttpClient.close_aiohttp_client()


app = FastAPI(debug=settings.DEBUG, on_startup=[on_startup], on_shutdown=[on_shutdown])
log = logging.getLogger(__name__)

app.include_router(root_api_router)
app.add_exception_handler(HTTPException, http_exception_handler)
