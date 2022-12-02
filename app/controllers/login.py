import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, UsersResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/login",
    tags=["users"],
    response_model=UsersResponse,
    summary="User login.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def login(email, password):
    log.info("POST /login")

    # Login user

    return UsersResponse(success=True, action="login")
