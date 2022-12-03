import logging

from fastapi import APIRouter, Depends, status

from app.exceptions.http import HTTPException, E
from app.models import BlockRequest, User
from app.utils import MongoDBClient, UserVerificationClient
from app.views import ErrorResponse, ReadyResponse
from pymongo import MongoClient

router = APIRouter()
log = logging.getLogger(__name__)


@router.post(
    "/block/create",
    tags=["blocks"],
    response_model=ReadyResponse,
    summary="Create a block.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def create_block(
    blockRequest: BlockRequest, 
    database: MongoClient = Depends(MongoDBClient.get_database),
    current_user: User = Depends(UserVerificationClient.get_current_user),
):
    log.info("POST /block/create")

    block = Block(
        type=blockRequest.type,
        properties=blockRequest.properties,
        content=[],  # TODO: add content
        editors=[database.users.find_one(email=current_user.email).get("_id")],
        parent=None,  # TODO: add parent
    )
    database.blocks.insert_one(block.dict())
    if block.type is BlockType.PAGE:
        database.users.update_one(
            # Update the user's owner page list.
            {"_id": current_user.id},
            {"$push": {"ownerPages": block.id}},
        )

    return ReadyResponse(status="ok")
