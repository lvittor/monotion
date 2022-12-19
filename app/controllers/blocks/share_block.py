import logging

from fastapi import APIRouter, Depends, status

from app.exceptions.http import HTTPException
from app.models import User
from app.models.block import Block, PydanticObjectId
from app.utils import UserVerificationClient
from app.utils.mongo_client import MongoDBClient
from app.views import BaseResponse, ErrorResponse

router = APIRouter()
log = logging.getLogger(__name__)

@router.put(
    "/block/{id}/share",
    tags=["blocks"],
    response_model=BaseResponse,
    summary="Share a block.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def share_block(
    id,
    user: User = Depends(UserVerificationClient.get_current_user),
    database = Depends(MongoDBClient.get_database)
):
    log.info(f"POST /block/{id}/share")

    block_id = PydanticObjectId.validate(id)
    block = database.blocks.find_one({"_id": block_id})
    block = Block(**block)
    user_id = database.users.find_one({"email": user.email})['_id']

    if str(user_id) != str(block.page_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            content=ErrorResponse(
                code=status.HTTP_403_FORBIDDEN,
                message="You cannot share a block that belongs to a page you do not own.",
            ).dict(exclude_none=True),
        )

    share_block_children(block, database)

    database.blocks.update_one({"_id": block_id}, {"$set": {"is_public": True}})
    block = database.blocks.find_one({"_id": block_id})
    block = Block(**block)
    return BaseResponse(
        success=True, properties={"block_id": str(block_id), "block": block.to_json()}
    )

def share_block_children(block, database):
    if not block.content:
        return

    for child in block.content:
        block = Block(**database.blocks.find_one({"_id": child}))

        share_block_children(block, database)

        database.blocks.update_one({"_id": child},{"$set": {"is_public": True}})
