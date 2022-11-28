import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.utils import PostgresClient
from app.views import ErrorResponse, ReadyResponse

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
    if not await PostgresClient.ping():
        log.error("Could not connect to Postgres")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                code=status.HTTP_502_BAD_GATEWAY,
                message="Could not connect to Postgres",
            ).dict(exclude_none=True),
        )

    return ReadyResponse(status="ok")
