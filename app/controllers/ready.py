import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.utils import MongoDBClient
from app.views import ErrorResponse, ReadyResponse
from app.settings import settings

router = APIRouter()
log = logging.getLogger(__name__)


@router.get(
    "/ready",
    tags=["ready"],
    response_model=ReadyResponse,
    summary="Simple health check.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def ready():
    log.info("GET /ready")
    if not await MongoDBClient.ping():
        log.error("Could not connect to MongoDB")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                code=status.HTTP_502_BAD_GATEWAY,
                message="Could not connect to MongoDB",
            ).dict(exclude_none=True),
        )

    return ReadyResponse(status=f"{settings.MONGO_URI}")
