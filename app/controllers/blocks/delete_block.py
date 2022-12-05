import logging

from fastapi import APIRouter, Depends, status

from app.exceptions.http import HTTPException
from app.models import User
from app.utils import MongoDBClient, UserVerificationClient
from app.views import BaseResponse, ErrorResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.delete(
    "/block/{id}/delete",
    tags=["blocks"],
    response_model=BaseResponse,
    summary="Delete a block.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def delete_block(
    id,
    user: User = Depends(UserVerificationClient.get_current_user),
    database=Depends(MongoDBClient.get_database),
):
    log.info(f"Delete /block/{id}/delete")

    # It should delete the block and al of its content. It should remove its ID
    # and its content blocks IDs. If it is a page, it should remove all of its references
    # in every existing user.
    # Inefficient

    return BaseResponse(success=True, properties={})
