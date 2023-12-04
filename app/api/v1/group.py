from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException


from app.schemas.group import (
    ViewGroup,
    GroupInDB,
    GroupCreate,
    GroupCreateWithMaster,
    GroupUpdate,
    GroupUpdateProtected,
)

from app.controllers import group as group_controller

from app.permissions import group as permissions

from app.utils.deps import identify_request, Profile

api = APIRouter()


@api.get('/', response_model=ViewGroup)
async def get_by_id(
    group_id: int
):
    if group := await group_controller.get_by_id(group_id):
        return group
    else:
        raise HTTPException(404)


@api.get('/my', response_model=List[GroupInDB])
async def get_by_user(
    identity: Profile = Depends(identify_request),
):
    if group := await group_controller.get_by_user(
        identity.user_profile_id,
    ):
        return group
    else:
        raise HTTPException(404)


@api.get('/by-user/private', response_model=List[GroupInDB])
async def get_by_user_private(
    real_user_id: int,
    identity: Profile = Depends(identify_request),
):
    if identity.is_admin:
        if group := await group_controller.get_by_user_verbouse(
            real_user_id
        ):
            return group
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.post('/', response_model=GroupInDB)
async def create(
    group: GroupCreate,
    identity: Profile = Depends(identify_request),
):
    if identity.master_id:
        group = GroupCreateWithMaster(
            master_id=identity.master_id,
            **group.model_dump(),
        )
        if group := await group_controller.create(
            group,
            # identity.user_profile_id,
        ):
            return group
    raise HTTPException(404)


@api.put('/', response_model=GroupInDB)
async def updapte(
    group_id: int,
    group: GroupUpdateProtected,
    identity: Profile = Depends(identify_request),
):
    if group := await group_controller.update(
        group,
        group_id,
        identity.master_id,
    ):
        return group
    else:
        raise HTTPException(404)


@api.put('/private', response_model=GroupInDB)
async def updapte_private(
    group_id: int,
    group: GroupUpdate,
    identity: Profile = Depends(identify_request),
):
    if identity.is_admin:
        if group := await group_controller.update(
            group,
            group_id,
        ):
            return group
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.put('/master', response_model=GroupInDB)
async def updapte_with_master_privilege(
    group_id: int,
    group: GroupUpdate,
    identity: Profile = Depends(identify_request),
):
    if await permissions.is_group_master(group_id, identity):
        if group := await group_controller.update(
            group,
            group_id,
        ):
            return group
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.delete('/master', response_model=GroupInDB)
async def delete_with_master_privilege(
    group_id: int,
    identity: Profile = Depends(identify_request),
):
    if await permissions.is_group_master(group_id, identity):
        if group := await group_controller.delete(
            group_id,
        ):
            return group
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.delete('/private', response_model=GroupInDB)
async def delete_with_admin_privilege(
    group_id: int,
    identity: Profile = Depends(identify_request),
):
    if identity.is_admin:
        if group := await group_controller.delete(
            group_id,
        ):
            return group
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)
