import logging

from fastapi import APIRouter, Depends, status
from pydantic.error_wrappers import ValidationError
from pymongo.errors import DuplicateKeyError

from app.exceptions.http import HTTPException
from app.models import User
from app.utils import MongoDBClient, UserVerificationClient, ElasticsearchClient
from app.views import BaseResponse, ErrorResponse

router = APIRouter()
log = logging.getLogger(__name__)

# TODO: You must only register only if you are not logged in
@router.post(
    "/register",
    tags=["users"],
    response_model=BaseResponse,
    summary="User registration.",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def register(
    email, username, password, database=Depends(MongoDBClient.get_database), es = Depends(ElasticsearchClient.get_client)
):
    log.info("POST /register")
    user_id = None
    hashed_password = UserVerificationClient.get_password_hash(password)
    try:
        user = User(email=email, username=username, password=hashed_password)
        user_id = database.users.insert_one(user.dict())
    except DuplicateKeyError:
        log.error(f"User with email: {email} already exists.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponse(
                code=status.HTTP_409_CONFLICT,
                message="User already exists.",
            ).dict(exclude_none=True),
        )
    except ValidationError:
        log.error(f"Email: {email} is not valid.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                code=status.HTTP_400_BAD_REQUEST,
                message=f"The email {email} is not a valid email.",
            ).dict(exclude_none=True),
        )
    
    es_dict = {'id': user.dict()['_id'], 'username': user.dict()['username']}
    es.index(index="user-index", document=ElasticsearchClient.to_json(es_dict))
    
    return BaseResponse(
        success=True,
        properties=user.dict(exclude_none=True),
    )
