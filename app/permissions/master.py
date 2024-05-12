from asyncpg import Connection

from app.core.configs import settings

from app.controllers import master as master_controllers
from app.controllers import user_profile as user_profile_controller


from app.schemas.master import (
    ViewMaster,
)

from app.schemas.user_profile import (
    UserProfileInDB
)


async def is_admin(
    identity: dict,
) -> ViewMaster:
    """ if i have 'admin' role or i am this master """
    if identity['role'] == settings.ADMIN_ROLE_STRING:
        return True


async def update(
    master_id: int,
    # real_user_id: int,
    identity: dict,
) -> ViewMaster:
    if identity['role'] == settings.ADMIN_ROLE_STRING:
        return True
    master = await master_controllers.get_by_id(master_id)
    if identity['sub'] == master.user_id:
        return True


# async def delete(
#     master_id: int,
#     # real_user_id: int,
#     identity: dict,
# ) -> ViewMaster:
#     """ if i have 'admin' role or i am this master """
#     if identity['role'] == settings.ADMIN_ROLE_STRING:
#         return True
#     master = await master_controllers.get_by_id(master_id)
#     if identity['sub'] == master.user_real_id:
#         return True
