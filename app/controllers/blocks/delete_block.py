import logging

from fastapi import APIRouter, Depends, status

from app.exceptions.http import HTTPException
from app.models import User
from app.utils import MongoDBClient, UserVerificationClient
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
async def delete_block(
    id,
    user: User = Depends(UserVerificationClient.get_current_user),
    database=Depends(MongoDBClient.get_database),
):
    log.info(f"Delete /block/{id}")

    # Delete a block

    return ReadyResponse(status="ok")
