import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, ReadyResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.get(
    "/search/content/all",
    tags=["search"],
    response_model=ReadyResponse,
    summary="Search content across all blocks accessible by the current user.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def search_content_all():
    log.info(f"GET /search/content/all")
    
    # Get the content

    return ReadyResponse(status="ok")
