import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, ReadyResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/logout",
    tags=["users"],
    response_model=ReadyResponse,
    summary="User logout.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def logout():
    log.info("POST /logout")
    
    # Logout user

    return ReadyResponse(status="ok")