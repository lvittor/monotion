import logging

from fastapi import APIRouter, Depends, status
from pymongo import MongoClient

from app.exceptions.http import HTTPException
from app.models import Block, BlockRequest, BlockType, User
from app.utils import MongoDBClient, UserVerificationClient
from app.views import BaseResponse, ErrorResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/block/create",
    tags=["blocks"],
    response_model=BaseResponse,
    summary="Create a block.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def create_block(
    blockRequest: BlockRequest,
    database: MongoClient = Depends(MongoDBClient.get_database),
    user: User = Depends(UserVerificationClient.get_current_user),
):
    log.info("POST /block/create")

    user_id = database.users.find_one({"email": user.email})['_id']
    block = Block(creator=user_id, **blockRequest.dict())

    if await block.is_valid_block():
        block_id = database.blocks.insert_one(block.dict()).inserted_id

        if block.is_valid_page():  # Update the user's owner page list.
            database.users.update_one(
                {"_id": user_id},
                {"$push": {"pages": block_id}},
            )

        if block.parent:  # Update the parent block's children (i.e. content) list.
            database.blocks.update_one(
                {"_id": block.parent},
                {"$push": {"content": block_id}},
            )
    else:
        log.error(
            f"Block is invalid. Please check the blockRequest: {blockRequest.dict()}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                code=status.HTTP_400_BAD_REQUEST,
                message=f"Block is invalid. Please check the blockRequest: {blockRequest.dict()}",
            ).dict(exclude_none=True),
        )

    return BaseResponse(
        success=True, properties={"block_id": str(block_id), "block": block.to_json()}
    )
