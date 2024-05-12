from typing import Optional, List

from asyncpg import Connection

from fastapiplugins.controllers import (
    DatabaseManager as DM,
    unpack_data,
    select_q,
    insert_q,
    update_q,
    delete_q,
)

from app.schemas.master import (
    MasterInDB,
    ViewMaster,
    MasterCreate,
    MasterUpdate,
    MasterCreateWithMaster,
)


@DM.acqure_connection()
async def get_by_user_id(
    user_id: int,
    conn: Connection = None,
) -> ViewMaster:
    result = await conn.fetchrow(*select_q(
        'view_master',
        # ViewMaster,
        user_id=user_id,
    ))
    if not result:
        return result
    return ViewMaster(**result)


@DM.acqure_connection()
async def get_by_id(
    master_id: Optional[int] = None,
    conn: Connection = None,
) -> ViewMaster:
    result = await conn.fetchrow(*select_q(
        'view_master',
        id=master_id,
    ))
    if not result:
        return result
    return ViewMaster(**result)


@DM.acqure_connection()
async def get_user_id_for_bot_completion(
    conn: Connection = None,
) -> List[int]:
    users_ids = await conn.fetch(
        'select user_id from master',
    )
    if users_ids:
        return [record['user_id'] for record in users_ids]


# @DM.acqure_connection()
# async def get_all(
#     search_by: Optional[str] = None,
#     conn: Connection = None,
# ) -> ViewMaster:
#     if search_by:
#         result = await conn.fetch(
#             """
#             select * from view_master
#             where
#                 title like $1 or
#                 description like $1
#             order by
#                 is_approved desc nulls last,
#                 rating desc nulls last
#             """,
#             f'%{search_by}%'
#         )
#     else:
#         result = await conn.fetch(
#             """
#             select * from view_master
#             order by
#                 is_approved desc nulls last,
#                 rating desc nulls last
#             """,
#         )
#     if not result:
#         return result
#     return [ViewMaster(**row) for row in result]


@DM.acqure_connection()
async def get_page(
    limit: int,
    offset: int,
    search_by: Optional[str] = None,
    conn: Connection = None,
) -> ViewMaster:
    if not search_by:
        search_by = '_'
    result = await conn.fetch(
        """
        select * from view_master
        where
            title like $1 or
            description like $1
        order by
            is_approved desc nulls last,
             approvals_amount desc nulls last,
            rating desc nulls last
        limit $2 offset $3
        """,
        f'%{search_by}%',
        limit,
        offset,
    )
    if not result:
        return result
    return [ViewMaster(**row) for row in result]
    # return ViewMaster(**result[1])


# @DM.acqure_connection()
# async def get_by_fraction(
#     fraction_id: int,
#     limit: int,
#     offset: int,
#     conn: Connection = None,
# ) -> ViewMaster:
#     result = await conn.fetchrow(
#         'select '
#             '* '
#         'from '
#             'view_master '
#         'where fraction_id = $1 '
#         'limit $2 '
#         'offset $3 '
#         'order by rating, pinned',
#         fraction_id,
#         limit,
#         offset,
#     )
#     if not result:
#         return result
#     return ViewMaster(**result)


@DM.acqure_connection()
async def save(
    master_data: MasterCreateWithMaster,
    conn: Connection = None,
) -> MasterInDB:
    fields, values = unpack_data(master_data)
    result = await conn.fetchrow(
        *insert_q(
            master_data,
            'master'
        )
    )
    if not result:
        return result
    master = MasterInDB(**result)
    return master


@DM.acqure_connection()
async def update(
    master_id: int,
    master_data: MasterUpdate,
    conn: Connection = None,
) -> MasterInDB:
    result = await conn.fetchrow(
        *update_q(master_data, 'master', id=master_id)
    )
    if not result:
        return result
    master = MasterInDB(**result)
    return master


@DM.acqure_connection()
async def delete(
    master_id: int,
    conn: Connection = None,
) -> MasterInDB:
    result = await conn.fetchrow(
        *delete_q('master', id=master_id)
    )
    if not result:
        return result
    master = MasterInDB(**result)
    return master
