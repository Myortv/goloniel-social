from asyncpg import Connection

from fastapiplugins.controllers import (
    DatabaseManager as DM,
    # unpack_data,
    select_q,
    update_q,
    delete_q,
    insert_q,
)


from app.schemas.master_rating import RatingCreate, RatingInDB


@DM.acqure_connection()
async def get(
    master_id: int,
    user_profile_id: int,
    conn: Connection = None,
) -> None:
    result = await conn.fetchrow(
        *select_q(
            'master_rating',
            master_id=master_id,
            user_profile_id=user_profile_id,
        )
    )
    if not result:
        return result
    return RatingInDB(**result)


@DM.acqure_connection()
async def set(
    rating: RatingCreate,
    user_profile_id: int,
    conn: Connection = None,
) -> None:
    result = await conn.fetchrow(
        'insert into master_rating '
        '(user_profile_id, master_id, rating) '
        'values '
        '($1, $2, $3)'
        'on conflict on constraint  '
        'master_rating_user_profile_id_master_id_key '
        'do update set rating = $3 '
        'returning *',
        user_profile_id,
        rating.master_id,
        rating.rating,
    )
    if not result:
        return result
    return RatingInDB(**result)


@DM.acqure_connection()
async def delete(
    master_id: int,
    user_profile_id: int,
    conn: Connection = None,
) -> None:
    result = await conn.fetchrow(
        *delete_q(
            'master_rating',
            master_id=master_id,
            user_profile_id=user_profile_id,
        )
    )
    if not result:
        return result
    return RatingInDB(**result)

