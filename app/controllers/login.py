import logging

from datetime import timedelta

from fastapi import APIRouter, status, Depends

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, UsersResponse
from app.utils import MongoDBClient, UserVerificationClient
#token should be a view?
from app.models import User, Token


router = APIRouter()
log = logging.getLogger(__name__)


ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post(
    "/login",
    tags=["users"],
    response_model=Token,
    summary="User login.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def login(email, password, database=Depends(MongoDBClient.get_database)):
    log.info("POST /login")

    found = database.users.find_one({"email": email})
    
    if found is None:
        log.error(f"Incorrect username or password.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=ErrorResponse(
                code=status.HTTP_401_UNAUTHORIZED,
                message="Incorrect username or password.",
            ).dict(exclude_none=True),
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = User(**found)
    
    if not UserVerificationClient.verify_user(user.password, password):
        log.error(f"Incorrect username or password.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=ErrorResponse(
                code=status.HTTP_401_UNAUTHORIZED,
                message="Incorrect username or password.",
            ).dict(exclude_none=True),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserVerificationClient.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    # Login user
    return Token(access_token=access_token, token_type="bearer")
