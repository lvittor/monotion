import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, ReadyResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.delete(
    "/block/{id}",
    tags=["blocks"],
    response_model=ReadyResponse,
    summary="Delete a block.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def delete_block(id):
    log.info(f"Delete /block/{id}")
    
    # Delete a block

    return ReadyResponse(status="ok")
