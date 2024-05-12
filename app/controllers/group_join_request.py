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

from app.controllers import group_membership as membership_controller

from app.utils.controllers import create_optional_filters


@DM.acqure_connection()
async def get(
    group_id: int,
    user_id: int,
    conn: Connection = None,
) -> GroupMembershipRequestInDB:
    result = await conn.fetchrow(
        *select_q(
            'squad_membership_request',
            squad_id=group_id,
            user_id=user_id,
        )
    )
    if not result:
        return result
    return GroupMembershipRequestInDB(**result)


@DM.acqure_connection()
async def get_by_id(
    join_request_id: int,
    conn: Connection = None,
) -> GroupMembershipRequestInDB:
    result = await conn.fetchrow(
        *select_q(
            'squad_membership_request',
            id=join_request_id,
        )
    )
    if not result:
        return result
    return GroupMembershipRequestInDB(**result)


@DM.acqure_connection()
async def get_search_page_by_master(
    master_id: int,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    group_id: Optional[int] = None,
    user_id: Optional[int] = None,
    is_full: Optional[bool] = None,
    is_accepted: Optional[bool] = None,
    conn: Connection = None,
) -> List[GroupMembershipRequestInDB]:
    index = 1
    filters, args, index = create_optional_filters(
        index,
        master_id=master_id,
        is_full=is_full,
        is_accepted=is_accepted,
        squad_id=group_id,
        user_id=user_id,
    )
    result = await conn.fetch(
        f"""
        select squad_membership_request.* from squad_membership_request
        left join squad
        on squad.id = squad_membership_request.squad_id
        where
        {' and '.join(filters)}
        order by squad_membership_request.created_at desc
        limit ${index} offset ${index+1}
        """,
        *args,
        limit,
        offset,
    )
    if not result:
        return result
    return [
        GroupMembershipRequestInDB(**row)
        for row in result
    ]


@DM.acqure_connection()
async def get_search_page_by_user(
    user_id: int,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    is_full: Optional[bool] = None,
    is_accepted: Optional[bool] = None,
    group_id: Optional[int] = None,
    conn: Connection = None,
) -> List[GroupMembershipRequestInDB]:
    index = 1
    filters, args, index = create_optional_filters(
        index,
        user_id=user_id,
        is_full=is_full,
        is_accepted=is_accepted,
        squad_id=group_id,
    )
    result = await conn.fetch(
        f"""
        select squad_membership_request.* from squad_membership_request
        left join squad
        on squad.id = squad_membership_request.squad_id
        where
        {' and '.join(filters)}
        order by squad_membership_request.created_at desc
        limit ${index} offset ${index+1}
        """,
        *args,
        limit,
        offset,
    )
    if not result:
        return result
    return [
        GroupMembershipRequestInDB(**row)
        for row in result
    ]


@DM.acqure_connection()
async def get_by_group(
    group_id: int,
    conn: Connection = None,
) -> List[GroupMembershipRequestInDB]:
    result = await conn.fetch(
        # 'select '
        #     'squad_membership_request.* '
        # 'from squad_membership_request '
        # 'left join squad '
        # 'on squad_membership_request.squad_id = squad.id '
        # 'where squad.id = $1 and sqaud.master_id = $2 '
        # 'order by is_accepted ',
        """
        select squad_membership_request.* from squad_membership_request
        where
        squad_id = $1
        -- offset $2 limit $2
        order by is_accepted, created_at
        """,
        group_id,
    )
    if not result:
        return result
    return [
        GroupMembershipRequestInDB(**row)
        for row in result
    ]


# @DM.acqure_connection()
# async def get_requests_by_master(
#     # squad_id: int,
#     master_id: int,
#     conn: Connection = None,
# ) -> List[GroupMembershipRequestInDB]:
#     result = await conn.fetch(
#         'select '
#             'squad_membership_request.* '
#         'from squad_membership_request '
#         'left join squad '
#         'on squad_membership_request.squad_id = squad.id '
#         'where squad.master_id = $1 '
#         'order by squad_membership_request.is_accepted ',
#         master_id,
#     )
#     if not result:
#         return result
#     return [
#         GroupMembershipRequestInDB(**row)
#         for row in result
#     ]


@DM.acqure_connection()
async def create(
    request: GroupMembershipRequestCreate,
    conn: Connection = None,
) -> GroupMembershipRequestInDB:
    result = await conn.fetchrow(
        *insert_q(request, 'squad_membership_request')
    )
    if not result:
        return result
    return GroupMembershipRequestInDB(**result)


@DM.acqure_connection()
async def delete(
    group_id: int,
    user_id: int,
    conn: Connection = None,
) -> GroupMembershipRequestInDB:
    result = await conn.fetchrow(
        *delete_q(
            'squad_membership_request',
            squad_id=group_id,
            user_id=user_id,
        )
    )
    if not result:
        return result
    return GroupMembershipRequestInDB(**result)


@DM.acqure_connection()
async def update(
    request_id: int,
    request: GroupMembershipRequestUpdate,
    conn: Connection = None,
) -> GroupMembershipRequestInDB:
    result = await conn.fetchrow(
        *update_q(request, 'squad_membership_request', id=request_id)
    )
    if not result:
        return result
    return GroupMembershipRequestInDB(**result)


@DM.acqure_connection()
async def accept(
    request_id: int,
    join_request: GroupMembershipRequestInDB,
    conn: Connection = None,
) -> LnkGroupUserInDB:
    tr = conn.transaction()
    await tr.start()
    try:
        request = await update(
            request_id,
            join_request,
            conn=conn,
        )
        if not request:
            await tr.rollback()
            return
        relation = await membership_controller.create(
            LnkGroupUserCreate(
                user_id=request.user_id,
                squad_id=request.squad_id,
                conn=conn
            )
        )
        if not relation:
            await tr.rollback()
            return
        await tr.commit()
        return relation
    except Exception as e:
        await tr.rollback()
        raise e
