from typing import Optional

from asyncpg import Connection


from fastapiplugins.controllers import (
    DatabaseManager as DM,
    insert_q,
    select_q_detailed,
    select_q,
    update_q,
    delete_q,
)

from app.schemas.user_profile import (
    UserProfileInDB,
    ViewProfile,
)


@DM.acqure_connection()
async def get(
    user_id: int,
    conn: Connection = None,
) -> UserProfileInDB:
    result = await conn.fetchrow(*select_q(
        'user_profile',
        id=user_id,
    ))
    if not result:
        return result
    return UserProfileInDB(**result)


# @DM.acqure_connection()
# async def _get_full_profile(
#     real_user_id: int,
#     conn: Connection = None,
# ) -> UserProfileInDB:
#     result = await conn.fetchrow(*select_q(
#         'view_profile',
#         real_id=real_user_id,
#     ))
#     return result


@DM.acqure_connection()
async def save(
    user_id: int,
    conn: Connection = None,
) -> UserProfileInDB:
    result = await conn.fetchrow(
        'insert into '
            'user_profile (id) '
        'values '
            '($1) '
        'returning * ',
        user_id,
    )
    if not result:
        return result
    return UserProfileInDB(**result)


@DM.acqure_connection()
async def delete(
    user_id: int,
    conn: Connection = None,
) -> UserProfileInDB:
    result = await conn.fetchrow(
        'delete from '
            'user_profile '
        'where '
            'id = $1 '
        'returning * ',
        user_id,
    )
    if not result:
        return result
    return UserProfileInDB(**result)


# @DM.acqure_connection()
# async def create(
#     real_user_id: int,
#     conn: Connection = None,
# ) -> UserProfileInDB:
#     result = await conn.fetchrow(*select_q(
#         'user_profile',
#         UserProfileInDB,
#         real_id=real_user_id,
#     ))
#     if not result:
#         return result
#     return UserProfileInDB(**result)
 
