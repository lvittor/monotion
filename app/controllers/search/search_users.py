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
    "/search/users",
    tags=["search"],
    response_model=SearchResponse,
    summary="Search users across all users.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def search_users(
    search: str,
    database: MongoClient = Depends(MongoDBClient.get_database),
    user: User = Depends(UserVerificationClient.get_current_user),
    es: ElasticsearchClient = Depends(ElasticsearchClient.get_client)
):
    log.info(f"GET /search/users")

    query = "(username:*{search}*)".format(search=search)
    resp = es.search(index='user-index', query={"query_string": {"query": query}})

    return SearchResponse(status="ok", data={'total': resp['hits']['total']['value'], 'data': resp['hits']['hits']})
