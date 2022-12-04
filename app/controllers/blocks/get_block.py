import logging

from fastapi import APIRouter, Depends, status

from app.exceptions.http import HTTPException
from app.models import User
from app.models.block import Block, PydanticObjectId
from app.utils import MongoDBClient, UserVerificationClient
from app.views import BaseResponse, ErrorResponse, ReadyResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.get(
    "/block/{id}",
    tags=["blocks"],
    response_model=BaseResponse,
    summary="Get the block content.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def get_block(
    id,
    user: User = Depends(UserVerificationClient.get_current_user),
    database=Depends(MongoDBClient.get_database),
):
    log.info(f"GET /block/{id}")
    block_id = PydanticObjectId.validate(id)
    block = database.blocks.find_one({"_id": block_id})
    block = Block(**block)
    user = User(**user)
    if id in user.get_all_allowed_blocks():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=ErrorResponse(
                code=status.HTTP_401_UNAUTHORIZED,
                message="Unauthorized access to block.",
            ).dict(exclude_none=True),
        )

    return BaseResponse(success=True, properties={"block": block.to_json()})
