import logging

from fastapi import APIRouter, status, Depends

from app.exceptions.http import HTTPException
from app.views import ErrorResponse, UsersResponse
from app.utils import UserVerificationClient

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/logout",
    tags=["users"],
    response_model=UsersResponse,
    summary="User logout.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def logout(current_user = Depends(UserVerificationClient.get_current_user)):
    log.info("POST /logout")

    # Expire jwt token and logout user

    return None

