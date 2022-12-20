import logging

from fastapi import APIRouter, Depends, status

from app.controllers.blocks.delete_block import remove_block_children
from app.models import Block, User
from app.utils import MongoDBClient, UserVerificationClient, ElasticsearchClient
from app.views import BaseResponse, ErrorResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.delete(
    "/unregister",
    tags=["users"],
    response_model=BaseResponse,
    summary="Unregister user.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def unregister(
    user: User = Depends(UserVerificationClient.get_current_user),
    database=Depends(MongoDBClient.get_database),
    es=Depends(ElasticsearchClient.get_client),
):
    log.info("POST /unregister")

    found = database.users.find_one({"email": user.email})

    deleted_user = {
        "email": f"{found['email']}",
        "username": f"{found['username']}",
        "deleted_pages": [],
    }

    for page in user.pages:
        block = Block(**database.blocks.find_one({"_id": page}))
        remove_block_children(block, database, es)
        deleted_user["deleted_pages"].append(str(page))
        database.blocks.delete_one({"_id": page})
        es_block_id = es.search(index='title-index', query={"query_string": {"query": "id:{block_id}".format(block_id=str(page))}})['hits']['hits'][0]['_id']
        es.delete(index='title-index', id=es_block_id)  # remove the block from the elastic search index

    database.users.delete_one({"_id": found["_id"]})

    es_user_id = es.search(index="user-index", query={"query_string": {"query": "id:{id}".format(id=found["_id"])}})['hits']['hits'][0]['_id']
    es.delete(index="user-index", id=es_user_id)

    return BaseResponse(success=True, properties={"deleted_user": deleted_user})
