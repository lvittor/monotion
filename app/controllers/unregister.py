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
    summary="Unregister user.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def unregister(
    user: User = Depends(UserVerificationClient.get_current_user),
    database=Depends(MongoDBClient.get_database)
):
    log.info("POST /unregister")

    found = database.users.find_one({"email": user.email})
    database.users.delete_one({"_id": found["_id"]})

    # Podríamos catchear la excepción de la base de datos en caso de que no se pueda
    # hacer la modificación
    # if not response.acknowledged:
    #     raise Exception:

    deleted_user = {
        "deleted_user": {
            "email": f"{found['email']}",
            "username": f"{found['username']}"
        }
    }
    return UsersResponse(success=True, properties={"deleted_user": deleted_user})