import logging

from fastapi import APIRouter, Depends, status
from pymongo.errors import DuplicateKeyError

from app.exceptions.http import HTTPException
from app.models import User
from app.utils import MongoDBClient, UserVerificationClient
from app.views import ErrorResponse, UsersResponse

router = APIRouter()
log = logging.getLogger(__name__)

@router.delete(
    "/unregister",
    tags=["users"],
    response_model=UsersResponse,
    summary="User logout.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def unregister(email, database=Depends(MongoDBClient.get_database)):
    log.info("POST /unregister")

    found = database.users.find_one({"email": email})
    response = database.users.delete_one({"_id": found["_id"]})

    if not response.acknowledged:
        # raise exception as invalid operation was triggered
        raise HTTPException()

    deleted_user = {
        "deleted_user": {
            "email": f"{found['email']}",
            "username": f"{found['username']}"
        }
    }
    return UsersResponse(success=True, properties={"deleted_user": deleted_user})