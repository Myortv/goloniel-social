from typing import List, Optional
import logging

from asyncpg import Connection

from fastapiplugins.controllers import (
    DatabaseManager as DM,
    select_q,
    insert_q,
    update_q,
    delete_q,
)

from app.schemas.group_membership import (
    LnkGroupUserInDB,
    LnkGroupUserCreate,
    GroupMembershipRequestInDB,
    GroupMembershipRequestCreate,
    GroupMembershipRequestUpdate,
)

from app.core.configs import settings

from app.utils.controllers import create_optional_filters


@DM.acqure_connection()
async def get_by_id(
    squad_id: int,
    real_user_id: int,
    conn: Connection = None,
) -> LnkGroupUserInDB:
    result = await conn.fetchrow(
        'with profile as ('
            'select '
                'id '
            'from user_profile '
            'where real_id = $1 '
        ') '
        'select '
            'lnk_squad_user.* '
        'from lnk_squad_user '
        'where squad_id = $2 and '
        'user_id = (select id from profile) ',
        real_user_id,
        squad_id,
    )
    if not result:
        return result
    return LnkGroupUserInDB(**result)


@DM.acqure_connection()
async def get_by_group(
    squad_id: int,
    conn: Connection = None,
) -> List[LnkGroupUserInDB]:
    result = await conn.fetch(
        *select_q(
            'lnk_squad_user',
            ['created_at'],
            squad_id=squad_id,
        )
    )
    if not result:
        return result
    return [LnkGroupUserInDB(**row) for row in result]


@DM.acqure_connection()
async def delete(
    squad_id: int,
    user_id: int,
    conn: Connection = None,
) -> LnkGroupUserInDB:
    result = await conn.fetchrow(
        *delete_q(
            'lnk_squad_user',
            squad_id=squad_id,
            user_id=user_id,
        )
    )
    if result:
        return LnkGroupUserInDB(**result)


@DM.acqure_connection()
async def delete_verbouse(
    squad_id: int,
    real_user_id: int,
    conn: Connection = None,
) -> LnkGroupUserInDB:
    result = await conn.fetchrow(
        'with profile as ('
            'select '
                'id '
            'from user_profile '
            'where real_id = $1 '
        ') '
        'delete from lnk_user_group '
        'where squad_id = $2 and '
        'user_id = (select id from profile) '
        'returning * ',
        squad_id,
        real_user_id,
    )
    if not result:
        return result
    return LnkGroupUserInDB(**result)


@DM.acqure_connection()
async def create(
    lnk_squad_user: dict | LnkGroupUserCreate,
    conn: Connection = None,
) -> LnkGroupUserInDB:
    result = await conn.fetchrow(
        *insert_q(
            lnk_squad_user,
            'lnk_squad_user'
        )
    )
    if not result:
        return result
    return LnkGroupUserInDB(**result)
