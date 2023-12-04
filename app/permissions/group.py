# from app.core.configs import settings

# from app.controllers import master as master_controllers
# from app.controllers import user_profile as user_profile_controller
# from app.controllers import group_membership as membership_controller
from app.controllers import group as group_controller

from app.utils.deps import Profile

# from app.schemas.master import (
#     ViewMaster,
# )

# from app.schemas.user_profile import (
#     UserProfileInDB
# )


async def is_group_master(
    group_id: int,
    identity: Profile,
) -> bool:
    group = await group_controller.get_by_id(
        group_id
    )
    if not identity.master_id:
        return False
    return group.master_id == identity.master_id


async def is_request_group_master(
    request_id: int,
    identity: Profile,
) -> bool:
    group = await group_controller.get_by_request(
        request_id,
    )
    return group.master_id == identity.master_id
