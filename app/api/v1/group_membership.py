from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException


from app.schemas.group_membership import (
    LnkGroupUserInDB,
    GroupMembershipRequestInDB,
    GroupMembershipRequestUpdate,
)

from app.controllers import group_membership as membership_controller

from app.permissions import group as permissions

# from app.messages import group as group_messages

from app.utils.deps import identify_request, Profile

api = APIRouter()


@api.get('/request', response_model=GroupMembershipRequestInDB)
async def get_request(
    group_id: int,
    identity: Profile = Depends(identify_request),
):
    """ all outgoing requests """
    print(identity)
    if request := await membership_controller.get_request(
        group_id,
        identity.user_profile_id

    ):
        return request
    else:
        raise HTTPException(404)


@api.get(
    '/request/by-user/private',
    response_model=List[GroupMembershipRequestInDB],
)
async def get_request_by_user_id(
    user_profile_id: int,
    identity: Profile = Depends(identify_request),
):
    """ all outgoing requests """
    if identity.is_admin:
        if group := await membership_controller.get_requests_by_user(
            user_profile_id,
        ):
            return group
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.get(
    '/request/by-user/me',
    response_model=List[GroupMembershipRequestInDB],
)
async def get_my_requests(
    identity: Profile = Depends(identify_request),
):
    """ all outgoing requests """
    if group := await membership_controller.get_requests_by_user(
        identity.user_profile_id,
    ):
        return group
    else:
        raise HTTPException(404)


@api.get(
    '/request/incoming/by-group',
    response_model=List[GroupMembershipRequestInDB]
)
async def get_requests_by_group(
    group_id: int,
    identity: Profile = Depends(identify_request),
):
    """ all incoming requests """
    if not identity.master_id:
        raise HTTPException(403)
    if group := await membership_controller.get_requests_by_group(
        group_id,
        identity.master_id,
    ):
        return group
    else:
        raise HTTPException(404)


@api.get(
    '/request/incoming/by-master',
    response_model=List[GroupMembershipRequestInDB]
)
async def get_requests_by_master(
    identity: Profile = Depends(identify_request),
):
    """ all incoming requests """
    if not identity.master_id:
        raise HTTPException(403)
    if group := await membership_controller.get_requests_by_master(
        identity.master_id,
    ):
        return group
    else:
        raise HTTPException(404)


@api.get(
    '/request/incoming/by-master/private',
    response_model=List[GroupMembershipRequestInDB],
)
async def get_requests_by_master_private(
    master_id: int,
    identity: Profile = Depends(identify_request),
):
    """ all incoming requests """
    if identity.is_admin:
        if group := await membership_controller.get_requests_by_master(
            master_id,
        ):
            return group
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.post('/request', response_model=GroupMembershipRequestInDB)
async def create_request(
    group_id: int,
    identity: Profile = Depends(identify_request),
):
    # """ all incoming requests """
    # if identity.is_admin:
    if group := await membership_controller.create_request(
        {"group_id": group_id, "user_profile_id": identity.user_profile_id},
    ):
        return group
    else:
        raise HTTPException(404)
    # else:
    #     raise HTTPException(403)


@api.delete('/request', response_model=GroupMembershipRequestInDB)
async def delete_request(
    group_id: int,
    identity: Profile = Depends(identify_request),
):
    # """ all incoming requests """
    # if identity.is_admin:
    if group := await membership_controller.delete_request(
         group_id, identity.user_profile_id,
    ):
        return group
    else:
        raise HTTPException(404)
    # else:
    #     raise HTTPException(403)


@api.put('/request/master', response_model=GroupMembershipRequestInDB)
async def update_request(
    request_id: int,
    request: GroupMembershipRequestUpdate,
    identity: Profile = Depends(identify_request),
):
    """ all incoming requests """
    if identity.is_admin:
        if request := await membership_controller.update_request(
            request_id,
            request,
        ):
            return request
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.get('/', response_model=LnkGroupUserInDB)
async def get_by_id(
    group_id: int,
    real_user_id: int,
):
    if group := await membership_controller.get_by_id(
        group_id,
        real_user_id,
    ):
        return group
    else:
        raise HTTPException(404)


@api.get('/by-group', response_model=LnkGroupUserInDB)
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
async def delete(
    group_id: int,
    identity: Profile = Depends(identify_request),
):
    if group := await membership_controller.delete(
        group_id,
        identity.user_profile_id,
    ):
        return group
    else:
        raise HTTPException(404)


@api.delete('/master', response_model=LnkGroupUserInDB)
async def delete_with_master_privilege(
    group_id: int,
    real_user_id: int,
    identity: Profile = Depends(identify_request),
):
    if await permissions.is_master(
        group_id,
        identity.master_id,
    ):
        if group := await membership_controller.delete_verbouse(
            group_id,
            real_user_id,
        ):
            return group
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.delete('/private', response_model=LnkGroupUserInDB)
async def delete_with_admin_privilege(
    group_id: int,
    real_user_id: int,
    identity: Profile = Depends(identify_request),
):
    if identity.is_admin:
        if group := await membership_controller.delete_verbouse(
            group_id,
            real_user_id,
        ):
            return group
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.post('/accept', response_model=LnkGroupUserInDB)
async def accept(
    request_id: int,
    identity: Profile = Depends(identify_request),
):
    """ accept users membersip request """
    if await permissions.is_request_group_master(
        request_id,
        identity,
    ):
        if request := await membership_controller.accept_request(
            request_id
        ):
            return request
        # if group := await membership_controller.create(
        #     group_id,
        #     identity.user_profile_id,
        # ):
        #     return group
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


# @api.create('/', response_model=lnkGroupUserInDB)
# async def create(
#     group_id: int,
#     identity: Profile = Depends(identify_request),
# ):
#     # check is master or admin
#     if group := await membership_controller.create(
#         group_id,
#         identity['sub'],
#     ):
#         return group
#     else:
#         raise HTTPException(404)


# @api.delete('/request', response_model=lnkGroupUserInDB)
# async def delete(
#     group_id: int,
#     identity: Profile = Depends(identify_request),
# ):
#     if group := await membership_controller.delete(
#         group_id,
#         identity['sub'],
#     ):
#         return group
#     else:
#         raise HTTPException(404)


# @api.delete('/', response_model=lnkGroupUserInDB)
# async def delete(
#     group_id: int,
#     identity: Profile = Depends(identify_request),
# ):
#     if group := await membership_controller.delete(
#         group_id,
#         identity['sub'],
#     ):
#         return group
#     else:
#         raise HTTPException(404)

