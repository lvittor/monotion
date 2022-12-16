import logging

from fastapi import APIRouter, Depends, status
from pymongo import MongoClient

from app.exceptions.http import HTTPException
from app.models.block import Block, PydanticObjectId
from app.models.user import User
from app.utils import MongoDBClient, UserVerificationClient
from app.views import BaseResponse, ErrorResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.put(
    "/block/{block_id}/share",
    tags=["blocks"],
    response_model=BaseResponse,
    summary="Share a block.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse}},
)
async def share_block(
    block_id,
    user_email,
    permission,
    database: MongoClient = Depends(MongoDBClient.get_database),
    user: User = Depends(UserVerificationClient.get_current_user),
):
    log.info(f"PUT /block/{block_id}/share")
    block_id = PydanticObjectId.validate(block_id)
    valid_perm = User.validate_shareable_permission(permission)
    if block_id not in user['ownerPages'] or not valid_perm:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            content=ErrorResponse(
                code=status.HTTP_403_FORBIDDEN,
                message="Unauthorized action over block.",
            ).dict(exclude_none=True),
        )

    if permission == "editor":
        database.users.update_one(
            {"email": user_email},
            {"$push": {"editorPages": block_id}},
        )

    if permission == "viewer":
        database.users.update_one(
            {"email": user_email},
            {"$push": {"viewerPages": block_id}},
        )

    block = database.blocks.find_one({"_id": block_id})
    # We don't need to validate block type, as in ownerPages will only be blocks with page type

    shared_with = database.users.find_one({"email": user_email})
    block = Block(**block)
    shared_with = User(**shared_with)

    return BaseResponse(
        success=True,
        properties={
            "shared_with_user": shared_with.to_json(),
            "block_id": str(block_id),
            "block": block.to_json(),
        },
    )
