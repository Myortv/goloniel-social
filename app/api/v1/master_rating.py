from fastapi import APIRouter, Depends
from fastapi import HTTPException


from fastapiplugins.exceptions import HandlableException

from app.controllers import master_rating as rating_controller

from app.utils.deps import identify_request, Profile

from app.schemas.master_rating import RatingCreate, RatingInDB


api = APIRouter()


@api.get('/private', response_model=RatingInDB)
async def get_vote(
    master_id: int,
    user_id: int,
    identity: Profile = Depends(identify_request),
):
    if not identity.is_admin:
        raise HTTPException(403)
    if rating := await rating_controller.get(
        master_id,
        user_id,
    ):
        return rating
    else:
        raise HTTPException(404)


@api.post('/private', response_model=RatingInDB)
async def set_my_vote(
    rating_create: RatingCreate,
    identity: Profile = Depends(identify_request),
):
    if not identity.is_admin:
        raise HTTPException(403)
    # if rating_create.master_id == identity.master_id:
    #     raise HandlableException(
    #         "SOCIAL-novoteformyself",
    #         422,
    #         short="You can't set any rating for yourself!"
    #     )
    if rating := await rating_controller.set(
        rating_create,
    ):
        return rating
    else:
        raise HTTPException(404)


@api.delete('/private', response_model=RatingInDB)
async def delete_my_vote(
    master_id: int,
    user_id: int,
    identity: Profile = Depends(identify_request),
):
    if not identity.is_admin:
        raise HTTPException(403)
    if rating := await rating_controller.delete(
        master_id,
        user_id,
    ):
        return rating
    else:
        raise HTTPException(404)


# @api.delete('/private', response_model=RatingInDB)
# async def delete_vote(
#     master_id: int,
#     user_id: int,
#     identity: Profile = Depends(identify_request),
# ):
#     if identity.is_admin:
#         if rating := await rating_controller.delete(
#             master_id,
#             user_id,
#         ):
#             return rating
#         else:
#             raise HTTPException(404)
#     else:
#         raise HTTPException(403)


# # @api.get('/', response_model=ViewMaster)
# # async def reset_rating(
# #     master_id: int,
# #     identity: dict = Depends(identify_request),
# # ):
# #     if ...:
# #         ...
# #     else:
# #         raise HTTPException(404)

