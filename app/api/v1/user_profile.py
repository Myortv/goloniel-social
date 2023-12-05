from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import HTTPException


from app.schemas.user_profile import (
    UserProfileInDB,
)

from app.controllers import user_profile as user_profile_controller

from app.utils.deps import parse_token

api = APIRouter()


@api.get('/', response_model=UserProfileInDB)
async def get_by_id(
    identity: dict = Depends(parse_token),
):
    if user_profile := await user_profile_controller.get(
        identity['sub'],
    ):
        return user_profile
    else:
        raise HTTPException(404)


@api.post('/', response_model=UserProfileInDB)
async def create_profile(
    identity: dict = Depends(parse_token),
):
    if user_profile := await user_profile_controller.save(
        identity['sub'],
    ):
        return user_profile
    else:
        raise HTTPException(404)


@api.delete('/', response_model=UserProfileInDB)
async def delete_profile(
    user_profile_id: Optional[int] = None,
    identity: dict = Depends(parse_token),
):
    """
    if no user_profile_id specified, all user profiles will be
    deleted
    """
    if user_profile := await user_profile_controller.delete(
        identity['sub'],
        user_profile_id,
    ):
        return user_profile
    else:
        raise HTTPException(404)
