import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, ReadyResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.get(
    "/block/{id}",
    tags=["blocks"],
    response_model=ReadyResponse,
    summary="Get the block content.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def get_block(id):
    log.info(f"GET /block/{id}")
    
    # Get block id

    return ReadyResponse(status="ok")
