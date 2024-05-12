from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi import HTTPException


from app.schemas.group import (
    GroupInDB,
    GroupCreate,
    GroupCreateWithMaster,
    GroupUpdate,
    GroupUpdateProtected,
)

from app.controllers import group as group_controller

from app.permissions import group as permissions

from app.utils.deps import (
    identify_request,
    Profile,
    # identify_user,
)

api = APIRouter()


@api.get('/', response_model=GroupInDB)
async def get_by_id(
    group_id: int
):
    if group := await group_controller.get_by_id(group_id):
        return group
    else:
        raise HTTPException(404)


@api.get('/page/search', response_model=List[GroupInDB])
async def get_page_search(
    master_id: Optional[int] = None,
    search_by: Optional[str] = None,
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
):
    if group := await group_controller.page_search(
        master_id,
        search_by,
        offset,
        limit,
    ):
        return group
    else:
        raise HTTPException(404)


@api.get('/page/by-user-id', response_model=List[GroupInDB])
async def get_page_by_user_id(
    user_id: int,
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
):
    if group := await group_controller.page_by_user_id(
        user_id,
        offset,
        limit,
    ):
        return group
    else:
        raise HTTPException(404)


@api.get('/page', response_model=List[GroupInDB])
async def get_page(
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
):
    if group := await group_controller.page(
        offset,
        limit,
    ):
        return group
    else:
        raise HTTPException(404)


@api.get('/by-master/', response_model=List[GroupInDB])
async def get_group_by_master_id(
    master_id: int,
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
):
    if group := await group_controller.get_by_master(
        master_id,
        offset,
        limit,
    ):
        return group
    else:
        raise HTTPException(404)


@api.get('/complete-title', response_model=List[dict])
async def complete_title():
    if titles := await group_controller.get_titles_complete():
        return titles
    else:
        raise HTTPException(404)

# @api.get('//by-title', response_model=List[ViewGroup])
# async def get_by_master_title(
#     group_title: str,
#     master_profile: Profile = Depends(identify_user),
# ):
#     if group := await group_controller.get_by_master_title(
#         master_profile.master_id,
#         group_title,
#     ):
#         return group
#     else:
#         raise HTTPException(404)


# @api.get('/by-master/raw/', response_model=List[GroupInDB])
# async def get_by_master(
#     master_profile: Profile = Depends(identify_user),
# ):
#     if groups := await group_controller.get_by_master(
#         master_profile.master_id
#     ):
#         return groups
#     else:
#         raise HTTPException(404)


# @api.get('/my', response_model=List[GroupInDB])
# async def get_by_user(
#     identity: Profile = Depends(identify_request),
# ):
#     if group := await group_controller.get_by_user(
#         identity.user_profile_id,
#     ):
#         return group
#     else:
#         raise HTTPException(404)


# @api.get('/by-user/private', response_model=List[GroupInDB])
# async def get_by_user_private(
#     real_user_id: int,
#     identity: Profile = Depends(identify_request),
# ):
#     if identity.is_admin:
#         if group := await group_controller.get_by_user_verbouse(
#             real_user_id
#         ):
#             return group
#         else:
#             raise HTTPException(404)
#     else:
#         raise HTTPException(403)


# @api.post('/', response_model=GroupInDB)
# async def create(
#     group: GroupCreate,
#     identity: Profile = Depends(identify_request),
# ):
#     if identity.master_id:
#         group = GroupCreateWithMaster(
#             master_id=identity.master_id,
#             **group.model_dump(),
#         )
#         if group := await group_controller.create(
#             group,
#         ):
#             return group
#     raise HTTPException(404)


# @api.put('/', response_model=GroupInDB)
# async def updapte(
#     group_id: int,
#     group: GroupUpdateProtected,
#     identity: Profile = Depends(identify_request),
# ):
#     if group := await group_controller.update(
#         group,
#         group_id,
#         identity.master_id,
#     ):
#         return group
#     else:
#         raise HTTPException(404)


# @api.put('/master', response_model=GroupInDB)
# async def updapte_with_master_privilege(
#     group_id: int,
#     group: GroupUpdate,
#     identity: Profile = Depends(identify_request),
# ):
#     if await permissions.is_group_master(group_id, identity):
#         if group := await group_controller.update(
#             group,
#             group_id,
#         ):
#             return group
#         else:
#             raise HTTPException(404)
#     else:
#         raise HTTPException(403)


# @api.delete('/master', response_model=GroupInDB)
# async def delete_with_master_privilege(
#     group_id: int,
#     identity: Profile = Depends(identify_request),
# ):
#     if await permissions.is_group_master(group_id, identity):
#         if group := await group_controller.delete(
#             group_id,
#         ):
#             return group
#         else:
#             raise HTTPException(404)
#     else:
#         raise HTTPException(403)


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
