import logging

from fastapi import APIRouter, Depends, status
from pymongo.errors import DuplicateKeyError

from app.exceptions.http import HTTPException
from app.models import User
from app.utils import MongoDBClient, UserVerificationClient
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
async def register(
    email, username, password, database=Depends(MongoDBClient.get_database)
):
    log.info("POST /register")
    hashed_password = UserVerificationClient.get_password_hash(password)
    user = User(email=email, username=username, password=hashed_password)
    try:
        database.users.insert_one(user.dict())
    except DuplicateKeyError:
        log.error(f"User with email: {email} already exists.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponse(
                code=status.HTTP_409_CONFLICT,
                message="User already exists.",
            ).dict(exclude_none=True),
        )
    return UsersResponse(
        success=True,
        properties=user.dict(exclude_none=True),
    )
