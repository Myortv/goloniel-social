from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from fastapiplugins.exceptions import HandlableException


from app.controllers import master_approval as approval_controller

from app.utils.deps import identify_request, Profile

from app.schemas.master_approval import (
    ApprovalInDB,
    ApprovalRequestInDB,
    # ApprovalRequestUpdateByOwner,
    ApprovalRequestUpdateByAdmin,
)

# from app.permissions import master as master_permissions


api = APIRouter()


""" approval -- vote for some master from other master or admin
    approval request -- request created from some master to be approved
"""


@api.get('/me', response_model=List[ApprovalInDB])
async def get_my_approvals(
    identity: Profile = Depends(identify_request),
):
    """
        returns approvals of me as a master
    """
    if identity.master_id:
        if approval := await approval_controller.get_approvals_by_master(
            identity.master_id
        ):
            return approval
    raise HTTPException(404)


@api.get('/', response_model=ApprovalInDB)
async def get_my_approve(
    master_id: int,
    identity: Profile = Depends(identify_request),
):
    """
        returns approval i give to master
    """
    if approval := await approval_controller.get(
        master_id,
        identity.user_profile_id,
    ):
        return approval
    else:
        raise HTTPException(404)


@api.get('/private', response_model=ApprovalInDB)
async def get_approve(
    master_id: int,
    user_profile_id: int,
    identity: Profile = Depends(identify_request),
):
    if identity.is_admin:
        if approval := await approval_controller.get(
            master_id,
            identity.user_profile_id,
        ):
            return approval
    raise HTTPException(404)


@api.get('/by-master/private', response_model=List[ApprovalInDB])
async def get_approvals_by_master(
    master_id: int,
    identity: Profile = Depends(identify_request),
):
    if identity.is_admin:
        if approval := await approval_controller.get_approvals_by_master(
            master_id,
        ):
            return approval
    raise HTTPException(404)


@api.post('/', response_model=ApprovalInDB)
async def set_my_approve(
    master_id: int,
    identity: Profile = Depends(identify_request),
):
    """
        create approval for some master
    """
    if master_id == identity.master_id:
        raise HandlableException(
            "SOCIAL-novoteformyself",
            422,
            short="You can't set any vote for yourself!"
        )
    if approval := await approval_controller.set_approval(
        master_id,
        identity.user_profile_id,
    ):
        return approval
    else:
        raise HTTPException(404)


@api.delete('/', response_model=ApprovalInDB)
async def delete_my_approve(
    master_id: int,
    identity: Profile = Depends(identify_request),
):
    """
        delete approval from some master
    """
    if approval := await approval_controller.delete(
        master_id,
        identity.user_profile_id,
    ):
        return approval
    else:
        raise HTTPException(404)


@api.get('/request/me', response_model=ApprovalRequestInDB)
async def get_approval_request(
    identity: Profile = Depends(identify_request),
):
    """
        get my approval request
    """
    if approval := await approval_controller.get_request(
        identity.master_id,
    ):
        return approval
    else:
        raise HTTPException(404)


@api.post('/request/me', response_model=ApprovalRequestInDB)
async def create_approval_request(
    identity: Profile = Depends(identify_request),
):
    """
        create approval request. approval request created for me as a master
    """
    if approval := await approval_controller.create_request(
        identity.master_id,
    ):
        return approval
    else:
        raise HTTPException(404)


@api.delete('/request/me', response_model=ApprovalRequestInDB)
async def delete_approval_request(
    identity: Profile = Depends(identify_request),
):
    """
        delete my approval request.
    """
    if approval := await approval_controller.delete_request(
        identity.master_id,
    ):
        return approval
    else:
        raise HTTPException(404)


# @api.put('/request/me', response_model=ApprovalRequestInDB)
# async def update_my_approval_request(
#     master_id: int,
#     request: ApprovalRequestUpdateByOwner,
#     identity: dict = Depends(identify_request),
# ):
#     """
#         update my approval request.
#     """
#     if approval := await approval_controller.update_request(
#         master_id,
#         request,
#         identity['sub'],
#     ):
#         return approval
#     else:
#         raise HTTPException(404)

# @api.put('/request/private', response_model=ApprovalRequestInDB)
# async def update_approval_request(
#     master_id: int,
#     request: ApprovalRequestUpdateByAdmin,
#     identity: Profile = Depends(identify_request),
# ):
#     if identity.is_admin:
#         if approval := await approval_controller.get_request(
#             master_id,
#         ):
#             return approval
#         else:
#             raise HTTPException(404)
#     else:
#         raise HTTPException(403)


@api.put('/request/private', response_model=ApprovalRequestInDB)
async def update_approval_request(
    master_id: int,
    request: ApprovalRequestUpdateByAdmin,
    identity: Profile = Depends(identify_request),
):
    """ update somebody's approval request as admin """
    # if await master_permissions.is_admin(identity):
    if identity.is_admin:
        if approval := await approval_controller.update_request(
            master_id,
            request,
        ):
            return approval
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)



# # @api.get('/', response_model=ViewMaster)
# # async def reset_approval(
# #     master_id: int,
# #     identity: dict = Depends(identify_request),
# # ):
# #     if ...:
# #         ...
# #     else:
# #         raise HTTPException(404)

