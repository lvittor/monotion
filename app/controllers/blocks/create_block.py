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
    current_user: User = Depends(UserVerificationClient.get_current_user),
):
    log.info("POST /block/create")
    current_user_id = database.users.find_one({"email": current_user['email']})['_id']
    print(type(current_user_id))
    block = Block(
        type=blockRequest.type,
        properties=blockRequest.properties,
        content=[],  # TODO: add content
        editors=[current_user_id],
        parent=None,  # TODO: add parent
    )
    print(block)
    print(block.dict())
    database.blocks.insert_one(block.dict())
    if block.type is BlockType.PAGE:
        database.users.update_one(
            # Update the user's owner page list.
            {"_id": current_user.id},
            {"$push": {"ownerPages": block.id}},
        )

    return BaseResponse(success=True, properties=block.to_json())
