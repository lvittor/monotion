import logging

from fastapi import APIRouter, Depends, status

from app.exceptions.http import HTTPException
from app.utils import UserVerificationClient
from app.views import BaseResponse, ErrorResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/logout",
    tags=["users"],
    response_model=BaseResponse,
    summary="User logout.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def logout(current_user=Depends(UserVerificationClient.get_current_user)):
    log.info("POST /logout")

    # Expire jwt token and logout user

    return None
