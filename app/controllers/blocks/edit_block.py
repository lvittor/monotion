import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, ReadyResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.put(
    "/block/edit/{id}",
    tags=["blocks"],
    response_model=ReadyResponse,
    summary="Edit a block.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def edit_block(id):
    log.info(f"PUT /block/edit/{id}")

    # Edit a block

    return ReadyResponse(status="ok")
