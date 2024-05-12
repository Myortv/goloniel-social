from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi import HTTPException


from app.schemas.group_membership import (
    LnkGroupUserInDB,
    GroupMembershipRequestInDB,
    GroupMembershipRequestUpdate,
    GroupMembershipRequestCreate,
)

# from app.controllers import group_membership as membership_controller
from app.controllers import group_join_request as join_request_controller

# from app.permissions import group as permissions

# from app.messages import group as group_messages

from app.utils.deps import identify_request, Profile
from fastapiplugins.exceptions import HandlableException

api = APIRouter()


@api.get('/', response_model=GroupMembershipRequestInDB)
async def get_request(
    group_id: int,
    user_id: int,
    identity: Profile = Depends(identify_request),
):
    """one specific request"""
    if not identity.is_admin:
        raise HTTPException(403)
    if request := await join_request_controller.get(
        group_id,
        user_id

    ):
        return request
    else:
        raise HTTPException(404)


@api.get('/by-id', response_model=GroupMembershipRequestInDB)
async def get_request_by_id(
    join_request_id: int,
    identity: Profile = Depends(identify_request),
):
    """one specific request"""
    if not identity.is_admin:
        raise HTTPException(403)
    if request := await join_request_controller.get_by_id(
        join_request_id

    ):
        return request
    else:
        raise HTTPException(404)


@api.get('/by-master', response_model=List[GroupMembershipRequestInDB])
async def get_requests_by_master_id(
    master_id: int,
    limit: int,
    offset: int,
    group_id: Optional[int] = None,
    user_id: Optional[int] = None,
    is_full: Optional[bool] = None,
    is_accepted: Optional[bool] = None,
    identity: Profile = Depends(identify_request),
):
    """ all requests related to specific user """
    if not identity.is_admin:
        raise HTTPException(403)
    if group := await join_request_controller.get_search_page_by_master(
        master_id,
        limit,
        offset,
        group_id,
        user_id,
        is_full,
        is_accepted,
     ):
        return group
    else:
        raise HTTPException(404)


@api.get('/by-user', response_model=List[GroupMembershipRequestInDB])
async def get_requests_by_user_id(
    user_id: int,
    limit: int,
    offset: int,
    is_full: Optional[bool] = None,
    is_accepted: Optional[bool] = None,
    group_id: Optional[int] = None,
    identity: Profile = Depends(identify_request),
):
    """ all requests related to specific user """
    if not identity.is_admin:
        raise HTTPException(403)
    if group := await join_request_controller.get_search_page_by_user(
        user_id,
        limit,
        offset,
        is_full,
        is_accepted,
        group_id,
     ):
        return group
    else:
        raise HTTPException(404)


@api.get('/by-group', response_model=List[GroupMembershipRequestInDB])
async def get_requests_by_group_id(
    group_id: int,
    identity: Profile = Depends(identify_request),
):
    """ all requests related to specific group """
    if not identity.is_admin:
        raise HTTPException(403)
    if group := await join_request_controller.get_by_group(
        group_id,
      ):
        return group
    else:
        raise HTTPException(404)


@api.post('/', response_model=GroupMembershipRequestInDB)
async def create_request(
    group: GroupMembershipRequestCreate,
    identity: Profile = Depends(identify_request),
):
    if not identity.is_admin:
        raise HTTPException(403)
    if group := await join_request_controller.create(
        group
    ):
        return group
    else:
        raise HTTPException(404)


@api.post('/accept', response_model=LnkGroupUserInDB)
async def accept_request(
    join_request_id: int,
    identity: Profile = Depends(identify_request),
):
    if not identity.is_admin:
        raise HTTPException(403)
    join_request = await join_request_controller.get_by_id(
        join_request_id,
    )
    if not join_request:
        raise HTTPException(404)
    join_request.is_accepted = True
    if lnk_group_user := await join_request_controller.accept(
        join_request_id,
        join_request,
    ):
        return lnk_group_user
    else:
        raise HTTPException(404)


@api.put('/', response_model=GroupMembershipRequestInDB)
async def update_request(
    join_requst_id: int,
    join_request: GroupMembershipRequestUpdate,
    identity: Profile = Depends(identify_request),
):
    if not identity.is_admin:
        raise HTTPException(403)
    if group := await join_request_controller.update(
        join_requst_id,
        join_request,
    ):
        return group
    else:
        raise HTTPException(404)


@api.delete('/', response_model=GroupMembershipRequestInDB)
async def delete_request(
    group_id: int,
    user_id: int,
    identity: Profile = Depends(identify_request),
):
    if not identity.is_admin:
        raise HTTPException(403)
    if group := await join_request_controller.delete_request(
         group_id,
         user_id,
    ):
        return group
    else:
        raise HTTPException(404)
