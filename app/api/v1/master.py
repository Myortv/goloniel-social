from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi import HTTPException


from app.schemas.master import (
    MasterInDB,
    ViewMaster,
    MasterCreate,
    MasterCreateProtected,
    MasterCreateWithMaster,
    MasterUpdate,
    MasterUpdateProtected,
)

from app.controllers import master as master_controller

# from app.permissions import master as permissions

# from app.messages import master as master_messages

from app.utils.deps import identify_request, Profile

api = APIRouter()


@api.get('/', response_model=ViewMaster)
async def get_by_id(
    master_id: int
):
    if master := await master_controller.get_by_id(master_id):
        return master
    else:
        raise HTTPException(404)


@api.get('/me', response_model=ViewMaster)
async def get_me(
    identity: Profile = Depends(identify_request),
):
    if identity.master_id:
        return await master_controller.get_by_id(identity.master_id)
    raise HTTPException(404)


@api.get('/page', response_model=List[ViewMaster])
async def get_page(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
):
    if master := await master_controller.get_page(
        limit, offset
    ):
        return master
    else:
        raise HTTPException(404)


# @api.get('/page/by-fraction', response_model=ViewMaster)
# async def get_page_by_fraction(
#     fraction_id: int,
#     limit: Optional[int] = 10,
#     offset: Optional[int] = 0,
# ):
#     if master := await master_controller.get_by_fraction(fraction_id):
#         return master
#     else:
#         raise HTTPException(404)


@api.post('/me', response_model=MasterInDB)
async def create_master(
    master_data: MasterCreateProtected,
    identity: Profile = Depends(identify_request),
):
    master_data = MasterCreateWithMaster(
        **master_data.model_dump(),
        user_profile_id=identity.user_profile_id
    )
    if master := await master_controller.save(
        master_data,
    ):
        return master
    else:
        raise HTTPException(404)


@api.post('/private', response_model=MasterInDB)
async def create_master_private(
    master_data: MasterCreate,
    identity: Profile = Depends(identify_request),
):
    if identity.is_admin:
        if master := await master_controller.save(master_data):
            return master
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.put('/me', response_model=MasterInDB)
async def update_master(
    master_data: MasterUpdateProtected,
    identity: Profile = Depends(identify_request),
):
    if master := await master_controller.update(
        identity.master_id,
        master_data,
    ):
        return master
    else:
        raise HTTPException(404)


@api.put('/private', response_model=MasterInDB)
async def update_master_private(
    master_id: int,
    master_data: MasterUpdate,
    identity: Profile = Depends(identify_request),
):
    if identity.is_admin:
        if master := await master_controller.update(
            master_id,
            master_data,
        ):
            return master
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)


@api.delete('/me', response_model=MasterInDB)
async def delete_master(
    identity: Profile = Depends(identify_request),
):
    if master := await master_controller.delete(identity.master_id):
        # await master_messages.emit_deleted(master)
        return master
    else:
        raise HTTPException(404)


@api.delete('/private', response_model=MasterInDB)
async def delete_master_private(
    master_id: int,
    identity: Profile = Depends(identify_request),
):
    if identity.is_admin:
        if master := await master_controller.delete(master_id):
            # await master_messages.emit_deleted(master)
            return master
        else:
            raise HTTPException(404)
    else:
        raise HTTPException(403)
