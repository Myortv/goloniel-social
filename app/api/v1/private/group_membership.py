from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi import HTTPException


from app.schemas.group_membership import (
    LnkGroupUserInDB,
    # GroupMembershipRequestInDB,
    # GroupMembershipRequestUpdate,
    # GroupMembershipRequestCreate,
)

from app.controllers import group_membership as membership_controller

from app.permissions import group as permissions

# from app.messages import group as group_messages

from app.utils.deps import identify_request, Profile

api = APIRouter()


@api.get('/by-group', response_model=List[LnkGroupUserInDB])
async def get_by_group(
    group_id: int,
):
    if group := await membership_controller.get_by_group(
        group_id,
    ):
        return group
    else:
        raise HTTPException(404)


@api.delete('/', response_model=LnkGroupUserInDB)
async def delete_request(
    group_id: int,
    user_id: int,
    identity: Profile = Depends(identify_request),
):
    # """ all incoming requests """
    if not identity.is_admin:
        raise HTTPException(403)
    if group := await membership_controller.delete(
         group_id,
         user_id,
    ):
        return group
    else:
        raise HTTPException(404)

