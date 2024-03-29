import logging

from fastapi import APIRouter, Depends, status
from pymongo import MongoClient

from app.exceptions.http import HTTPException
from app.models import User, Block, BlockRequest, BlockType
from app.models.block import PydanticObjectId
from app.utils import MongoDBClient, UserVerificationClient, ElasticsearchClient
from app.views import ErrorResponse, BaseResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.put(
    "/block/{id}/edit",
    tags=["blocks"],
    response_model=BaseResponse,
    summary="Edit a block.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def edit_block(
    id,
    block_request: BlockRequest,
    user: User = Depends(UserVerificationClient.get_current_user),
    database: MongoClient = Depends(MongoDBClient.get_database),
    es: ElasticsearchClient = Depends(ElasticsearchClient.get_client)
):
    log.info(f"PUT /block/edit/{id}")

    block_id = PydanticObjectId.validate(id)

    user_id = database.users.find_one({"email": user.email})['_id']
    block_db_info = database.blocks.find_one({"_id": block_id})
    block_db = Block(**block_db_info) if block_db_info else None

    if block_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(
                code=status.HTTP_404_NOT_FOUND,
                message="Block not found.",
            ).dict(exclude_none=True),
        )
    
    block = Block(creator=block_db.creator, page_owner=block_db.page_owner, **block_request.dict())

    if await block.is_valid_block():

        if not block_db.is_public and str(user_id) != str(block_db.creator):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                content=ErrorResponse(
                    code=status.HTTP_403_FORBIDDEN,
                    message="You have no permissions to edit this block.",
                ).dict(exclude_none=True),
            )

        database.blocks.update_one(
            {"_id": block_id},
            {"$set": {"properties": block.properties}}
        )

        updated_block = database.blocks.find_one({"_id": block_id})
        updated_block = Block(**updated_block)

        # get elastic id from elastic search
        if updated_block.type == BlockType.PAGE.value:
            update_dict = {"title": updated_block.properties['title']}
            es_block_id = es.search(index='title-index', query={"query_string": {"query": "id:{block_id}".format(block_id=str(block_id))}})['hits']['hits'][0]['_id']
            es.update(index='title-index', id=es_block_id, doc=ElasticsearchClient.to_json(update_dict))
        else:
            update_dict = {"properties": updated_block.properties}
            es_block_id = es.search(index='content-index', query={"query_string": {"query": "id:{block_id}".format(block_id=str(block_id))}})['hits']['hits'][0]['_id']
            es.update(index='content-index', id=es_block_id, doc=ElasticsearchClient.to_json(update_dict))
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                code=status.HTTP_400_BAD_REQUEST,
                message=f"Block is invalid. Please check the blockRequest: {block_request.dict()}",
            ).dict(exclude_none=True),
        )

    return BaseResponse(
        success=True, properties={"block_id": str(block_id), "block": updated_block.to_json()}
    )



    
