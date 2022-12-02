import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, ReadyResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/block/create",
    tags=["blocks"],
    response_model=ReadyResponse,
    summary="Create a block.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def create_block(id):
    log.info("POST /block/create")
    
    # Create a block

    return ReadyResponse(status="ok")
