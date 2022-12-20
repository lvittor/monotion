import logging

from fastapi import APIRouter, Depends, status
from pymongo import MongoClient

from app.exceptions.http import HTTPException
from app.models import User, Block
from app.views import ErrorResponse, SearchResponse
from app.utils import MongoDBClient, UserVerificationClient, ElasticsearchClient

router = APIRouter()
log = logging.getLogger(__name__)


@router.get(
    "/search/content",
    tags=["search"],
    response_model=SearchResponse,
    summary="Search content across all non page blocks accessible by the current user.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def search_content(
    search: str,
    database: MongoClient = Depends(MongoDBClient.get_database),
    user: User = Depends(UserVerificationClient.get_current_user),
    es: ElasticsearchClient = Depends(ElasticsearchClient.get_client)
):
    log.info(f"GET /search/content")

    user_id = database.users.find_one({"email": user.email})['_id']

    query = "(properties.text: *{search}*) AND ((is_public: true OR creator: {user_id}))".format(search=search, user_id=user_id)
    resp = es.search(index='content-index', query={"query_string": {"query": query}})

    return SearchResponse(status="ok", data={'total': resp['hits']['total']['value'], 'data': resp['hits']['hits']})
