import logging

from fastapi import APIRouter, Depends, status

from app.exceptions.http import HTTPException
from app.models import User
from app.models.block import Block, BlockType, PydanticObjectId
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

    block_id = PydanticObjectId.validate(id)
    block = database.blocks.find_one({"_id": block_id})
    user_id = database.users.find_one({"email": user.email})['_id']

    # check if the block exists
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(
                code=status.HTTP_404_NOT_FOUND,
                message="Block not found.",
            ).dict(exclude_none=True),
        )

    block = Block(**block)

    # check if the user has permissions to delete the block
    if not can_delete_block(user_id, block):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            content=ErrorResponse(
                code=status.HTTP_403_FORBIDDEN,
                message="You have not permissions to remove this block.",
            ).dict(exclude_none=True),
        )

    # remove the block from its' parent
    database.blocks.update_one({"_id": block.parent}, {"$pull": {"content": block_id}})

    # remove the block content (ie. it's children)
    remove_block_children(block, database)

    # remove the block
    database.blocks.delete_one({"_id": block_id})

    return BaseResponse(
        success=True, properties={"block_id": str(block_id), "block": block.to_json()}
    )


def can_delete_block(user_id, block):
    return block.creator == user_id


def remove_block_children(block, database):
    if not block.content:
        return

    for child in block.content:
        block = Block(**database.blocks.find_one({"_id": child}))  # get the block

        remove_block_children(block, database)  # go deeper

        database.blocks.delete_one({"_id": child})  # remove the block

        if block.type == BlockType.PAGE.value:
           database.users.update_one({"_id": block.page_owner}, {"$pull": {"pages": child}})  # remove the block from the user
