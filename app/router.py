"""Application configuration - root APIRouter.
    
Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications

"""

from fastapi import APIRouter

from app.controllers import login, logout, ready, register
from app.controllers.blocks import (
    create_block,
    delete_block,
    edit_block,
    get_block,
    share_block,
)
from app.controllers.search import search_content_all

root_api_router = APIRouter(prefix="/api")
root_api_router.include_router(ready.router, tags=["ready"])

root_api_router.include_router(login.router, tags=["users"])
root_api_router.include_router(logout.router, tags=["users"])
root_api_router.include_router(register.router, tags=["users"])

root_api_router.include_router(get_block.router, tags=["blocks"])
root_api_router.include_router(create_block.router, tags=["blocks"])
root_api_router.include_router(edit_block.router, tags=["blocks"])
root_api_router.include_router(delete_block.router, tags=["blocks"])
root_api_router.include_router(share_block.router, tags=["blocks"])

root_api_router.include_router(search_content_all.router, tags=["search"])
