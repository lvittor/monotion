import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, ReadyResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/block/share/{id}",
    tags=["blocks"],
    response_model=ReadyResponse,
    summary="Share a block.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def share_block(id):
    log.info(f"POST /block/share/{id}")

    # Share a block

    return ReadyResponse(status="ok")
