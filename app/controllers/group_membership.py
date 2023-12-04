from typing import List
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


@DM.acqure_connection()
async def get_request(
    group_id: int,
    user_profile_id: int,
    conn: Connection = None,
) -> GroupMembershipRequestInDB:
    result = await conn.fetchrow(
        *select_q(
            'group_membership_request',
            group_id=group_id,
            user_profile_id=user_profile_id,
        )
    )
    print(result)
    if not result:
        return result
    return GroupMembershipRequestInDB(**result)


@DM.acqure_connection()
async def get_requests_by_user(
    user_profile_id: int,
    conn: Connection = None,
) -> List[GroupMembershipRequestInDB]:
    result = await conn.fetch(
        *select_q(
            'group_membership_request',
            ['created_at'],
            user_profile_id=user_profile_id,
        )
    )
    if not result:
        return result
    return [
        GroupMembershipRequestInDB(**row)
        for row in result
    ]


@DM.acqure_connection()
async def get_requests_by_group(
    group_id: int,
    master_id: int,
    conn: Connection = None,
) -> List[GroupMembershipRequestInDB]:
    result = await conn.fetch(
        'select '
            'group_membership_request.* '
        'from group_membership_request '
        'left join playing_group '
        'on group_membership_request.group_id = playing_group.id '
        'where playing_group.id = $1 and playing_group.master_id = $2 '
        'order by is_accepted ',
        group_id,
        master_id,
    )
    if not result:
        return result
    return [
        GroupMembershipRequestInDB(**row)
        for row in result
    ]


@DM.acqure_connection()
async def get_requests_by_master(
    # group_id: int,
    master_id: int,
    conn: Connection = None,
) -> List[GroupMembershipRequestInDB]:
    result = await conn.fetch(
        'select '
            'group_membership_request.* '
        'from group_membership_request '
        'left join playing_group '
        'on group_membership_request.group_id = playing_group.id '
        'where playing_group.master_id = $1 '
        'order by group_membership_request.is_accepted ',
        master_id,
    )
    if not result:
        return result
    return [
        GroupMembershipRequestInDB(**row)
        for row in result
    ]


@DM.acqure_connection()
async def create_request(
    request: dict | GroupMembershipRequestCreate,
    conn: Connection = None,
) -> GroupMembershipRequestInDB:
    result = await conn.fetchrow(
        *insert_q(request, 'group_membership_request')
    )
    if not result:
        return result
    return GroupMembershipRequestInDB(**result)


@DM.acqure_connection()
async def delete_request(
    group_id: int,
    user_profile_id: int,
    conn: Connection = None,
) -> GroupMembershipRequestInDB:
    result = await conn.fetchrow(
        *delete_q(
            'group_membership_request',
            group_id=group_id,
            user_profile_id=user_profile_id,
        )
    )
    if not result:
        return result
    return GroupMembershipRequestInDB(**result)


@DM.acqure_connection()
async def update_request(
    request_id: int,
    request: GroupMembershipRequestUpdate,
    conn: Connection = None,
) -> GroupMembershipRequestInDB:
    result = await conn.fetchrow(
        *update_q(request, 'group_membership_request', id=request_id)
    )
    print(result)
    if not result:
        return result
    return GroupMembershipRequestInDB(**result)


@DM.acqure_connection()
async def accept_request(
    request_id: int,
    conn: Connection = None,
) -> LnkGroupUserInDB:
    tr = conn.transaction()
    await tr.start()
    try:
        request: GroupMembershipRequestInDB = await update_request(
            request_id,
            GroupMembershipRequestUpdate(
                state=settings.GROUP_MEMBERSHIP_REQUEST_ACCEPTED,
                is_accepted=True,
            ),
            conn=conn,
        )
        if not request:
            await tr.rollback()
            return
        link = await create(
            LnkGroupUserCreate(
                user_profile_id=request.user_profile_id,
                group_id=request.group_id,
                conn=conn
            )
        )
        if not link:
            await tr.rollback()
            return
        await tr.commit()
        return link
    except Exception as e:
        await tr.rollback()
        logging.exception(e)


@DM.acqure_connection()
async def get_by_id(
    group_id: int,
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
            'lnk_group_user.* '
        'from lnk_group_user '
        'where group_id = $2 and '
        'user_profile_id = (select id from profile) ',
        real_user_id,
        group_id,
    )
    if not result:
        return result
    return LnkGroupUserInDB(**result)


@DM.acqure_connection()
async def get_by_group(
    group_id: int,
    conn: Connection = None,
) -> LnkGroupUserInDB:
    result = await conn.fetchrow(
        *select_q(
            'lnk_group_user',
            ['created_at'],
            group_id=group_id,
        )
    )
    if not result:
        return result
    return [LnkGroupUserInDB(**row) for row in result]


@DM.acqure_connection()
async def delete(
    group_id: int,
    user_profile_id: int,
    conn: Connection = None,
) -> LnkGroupUserInDB:
    tr = conn.transaction()
    await tr.start()
    try:
        request = await delete_request(
            group_id,
            user_profile_id,
            conn=conn
        )
        if not request:
            await tr.rollback()
            return request

        result = await conn.fetchrow(
            *delete_q(
                'lnk_group_user',
                group_id=group_id,
                user_profile_id=user_profile_id,
            )
        )
        if not result:
            await tr.rollback()
            return result
        await tr.commit()
        return LnkGroupUserInDB(**result)
    except Exception as e:
        await tr.rollback()
        logging.exception(e)


@DM.acqure_connection()
async def delete_verbouse(
    group_id: int,
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
        'where group_id = $2 and '
        'user_profile_id = (select id from profile) '
        'returning * ',
        group_id,
        real_user_id,
    )
    if not result:
        return result
    return LnkGroupUserInDB(**result)


@DM.acqure_connection()
async def create(
    lnk_group_user: dict | LnkGroupUserCreate,
    conn: Connection = None,
) -> LnkGroupUserInDB:
    result = await conn.fetchrow(
        *insert_q(
            lnk_group_user,
            'lnk_group_user'
        )
    )
    if not result:
        return result
    return LnkGroupUserInDB(**result)
