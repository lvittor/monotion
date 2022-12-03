import logging

from fastapi import APIRouter, status, Depends

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, UsersResponse
from app.utils import UserVerificationClient
from app.models import User

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/me",
    tags=["users"],
    response_model=User,
    summary="Get current user.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def me(current_user: User = Depends(UserVerificationClient.get_current_user)):
    log.info("POST /me")

    # Get current user
    return current_user
    

