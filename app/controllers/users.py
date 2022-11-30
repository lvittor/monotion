import logging

from fastapi import APIRouter, status

from app.exceptions.http import HTTPException
from app.utils import PostgresClient
from app.views import ErrorResponse, UsersResponse

router = APIRouter()
log = logging.getLogger(__name__)

@router.post(
    "/login",
    tags=["login"],
    response_model=UsersResponse,
    summary="Log in existing user",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def login(email, password):
    log.info("POST /login")
    response_model=UserResponse(action="login")
    try:
        
    except Exception as e:
        log.error("Invalid user credentials")
        response_model.success=False
    return response_model

@router.post(
    "/logout",
    tags=["logout"],
    response_model=UsersResponse,
    summary="Log out existing user",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def logout():
    log.info("POST /logout")
    response_model=UserResponse(action="logout")
    try:
        
    except Exception as e:
        log.error("Unable to logout user")
        response_model.success=False
    return response_model

@router.post(
    "/signin",
    tags=["signin"],
    response_model=UsersResponse,
    summary="Sign in new user",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def signin(username, email, password):
    log.info("POST /signin")
    response_model=UserResponse(action="signin", success=True)
    try:
        
    except Exception as e:
        log.error("Invalid credentials")
        response_model.success=False
        response_model.email=email
        response_model.username=username
    return response_model