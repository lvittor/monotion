import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, UsersResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/register",
    tags=["users"],
    response_model=UsersResponse,
    summary="User registration.",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def register(email, username, password):
    log.info("POST /register")

    # Register the user

    return UsersResponse(properties={"email": f"{email}", "username": f"{username}", "password": f"{password}"})
