import logging

from fastapi import APIRouter, Depends, status
from pymongo import MongoClient

from app.exceptions.http import HTTPException
from app.models import Block, BlockRequest, BlockType, User
from app.utils import MongoDBClient, UserVerificationClient, ElasticsearchClient
from app.views import BaseResponse, ErrorResponse

import json

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
    es: ElasticsearchClient = Depends(ElasticsearchClient.get_client)
):
    log.info("POST /block/create")

    user_id = database.users.find_one({"email": user.email})['_id']
    block = Block(creator=user_id, page_owner=user_id, **blockRequest.dict())
    parent_block_info = database.blocks.find_one({"_id": block.parent})
    parent_block = Block(**parent_block_info) if parent_block_info else None

    if await block.is_valid_block():

        if parent_block and str(user_id) != str(parent_block.page_owner) and block.type == BlockType.PAGE.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                content=ErrorResponse(
                    code=status.HTTP_403_FORBIDDEN,
                    message="You have no permissions to create a page block in a public page.",
                ).dict(exclude_none=True),
            )

        block_id = database.blocks.insert_one(block.dict()).inserted_id
        page_owner = parent_block.page_owner if parent_block is not None else user_id
        database.blocks.update_one(
            {"_id": block_id},
            {"$set": {"page_owner": page_owner}}
        )

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

        if parent_block and parent_block.is_public:
            database.blocks.update_one(
                {"_id": block_id},
                {"$set": {"is_public": True}}
            )
        # TODO: verify if this is the only way to update object from db
        updated_block = database.blocks.find_one({"_id": block_id})
        updated_block = Block(**updated_block)

        if updated_block.type == BlockType.PAGE.value:
            dict_index = {"id": str(block_id), "title": updated_block.properties['title'], "is_public": updated_block.is_public, "page_owner": str(user_id)}
            es.index(index="title-index", document=ElasticsearchClient.to_json(dict_index))
        else:
            dict_index = {"id": str(block_id), "type": updated_block.type, "properties": updated_block.properties, "is_public": updated_block.is_public, "creator": str(user_id)}
            es.index(index="content-index", document=ElasticsearchClient.to_json(dict_index))

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
        success=True, properties={"block_id": str(block_id), "block": updated_block.to_json()}
    )
