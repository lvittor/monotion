import logging

from fastapi import APIRouter, Depends, status
from pymongo import MongoClient

from app.models import User
from app.utils import ElasticsearchClient, MongoDBClient, UserVerificationClient
from app.utils.parser import purge_page_data
from app.views import ErrorResponse, SearchResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.get(
    "/search/pages",
    tags=["search"],
    response_model=SearchResponse,
    summary="Search content across all pages accessible by the current user.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def search_pages(
    search: str,
    database: MongoClient = Depends(MongoDBClient.get_database),
    user: User = Depends(UserVerificationClient.get_current_user),
    es: ElasticsearchClient = Depends(ElasticsearchClient.get_client),
):
    log.info(f"GET /search/pages")

    user_id = database.users.find_one({"email": user.email})['_id']
    query = (
        "(title:*{search}*) AND ((is_public:true) OR (page_owner:{user_id}))".format(
            search=search, user_id=user_id
        )
    )
    resp = es.search(index='title-index', query={"query_string": {"query": query}})

    return SearchResponse(
        status="ok",
        data={
            'total': resp['hits']['total']['value'],
            'data': purge_page_data(resp['hits']['hits']),
        },
    )
