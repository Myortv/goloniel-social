from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import HTTPException


from app.schemas.user_profile import (
    UserProfileInDB,
    Profile
)

from app.controllers import user_profile as user_profile_controller

from app.utils.deps import identify_request

api = APIRouter()


@api.get('/', response_model=UserProfileInDB)
async def get_by_id(
    identity: Profile = Depends(identify_request),
):
    if user_profile := await user_profile_controller.get(
        identity.user_id,
    ):
        return user_profile
    else:
        raise HTTPException(404)


@api.post('/', response_model=UserProfileInDB)
async def create_profile(
    identity: Profile = Depends(identify_request),
):
    if user_profile := await user_profile_controller.save(
        identity.user_id,
    ):
        return user_profile
    else:
        raise HTTPException(404)


@api.delete('/', response_model=UserProfileInDB)
async def delete_profile(
    identity: Profile = Depends(identify_request),
):
    if user_profile := await user_profile_controller.delete(
        identity.user_id,
    ):
        return user_profile
    else:
        raise HTTPException(404)
