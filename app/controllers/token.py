from datetime import timedelta
import logging

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions.http import HTTPException
from app.models import Token, User
from app.settings import settings
from app.utils import MongoDBClient, UserVerificationClient
from app.views import ErrorResponse, UsersResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/token",
    tags=["users"],
    response_model=Token,
    summary="User login.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    database=Depends(MongoDBClient.get_database),
):
    log.info("POST /token")
    email = form_data.username
    password = form_data.password

    found = database.users.find_one({"email": email})

    if not found:
        log.error(f"Incorrect username or password.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            content=ErrorResponse(
                code=status.HTTP_401_UNAUTHORIZED,
                message="Incorrect username or password.",
            ).dict(exclude_none=True),
        )

    user = User(**found)

    if not UserVerificationClient.verify_user(user.password, password):
        log.error(f"Incorrect username or password.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            content=ErrorResponse(
                code=status.HTTP_401_UNAUTHORIZED,
                message="Incorrect username or password.",
            ).dict(exclude_none=True),
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserVerificationClient.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # Login user
    return Token(access_token=access_token, token_type="bearer")
