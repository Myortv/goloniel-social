from typing import List

from asyncpg import Connection

from fastapiplugins.controllers import (
    DatabaseManager as DM,
    unpack_data,
    select_q,
    update_q,
    delete_q,
    insert_q,
)

from app.schemas.master_approval import (
    ApprovalInDB,
    ApprovalRequestInDB,
    # ApprovalRequestUpdateByOwner,
    ApprovalRequestUpdateByAdmin,
)


@DM.acqure_connection()
async def get_approvals_by_master(
    master_id: int,
    conn: Connection = None,
) -> List[ApprovalInDB]:
    result = await conn.fetch(
        *select_q(
            'master_approvals',
            ['created_at'],
            master_id=master_id,
        )
    )
    if not result:
        return result
    return [ApprovalInDB(**row) for row in result]


@DM.acqure_connection()
async def get(
    master_id: int,
    user_profile_id: int,
    conn: Connection = None,
) -> ApprovalInDB:
    result = await conn.fetchrow(
        *select_q(
            'master_approvals',
            master_id=master_id,
            user_profile_id=user_profile_id
        )
    )
    if not result:
        return result
    return ApprovalInDB(**result)


@DM.acqure_connection()
async def set_approval(
    master_id: int,
    user_profile_id: int,
    conn: Connection = None,
) -> ApprovalInDB:
    result = await conn.fetchrow(
        # 'with master_profile as ( '
        #     'select id '
        #     'from master '
        #     'where user_profile_id = $1 '
        # '), insert_values as ( '
        #     'select '
        #         'id::int as user_profile_id, '
        #         '$1::int as master_id '
        #     'from '
        #         'user_profile  '
        #     'where '
        #         'user_profile.real_id = $2 '
        #             'and '
        #         '$1 != (select * from master_profile) '
        # ') '
        # 'insert into '
        #     'master_approvals '
        #         '(user_profile_id, master_id) '
        # '(select * from insert_values) '
        # 'returning * ',
        # master_id,
        # user_real_id,
        *insert_q(
            {"master_id": master_id, "user_profile_id": user_profile_id},
            'master_approvals',
        )
    )
    if not result:
        return result
    return ApprovalInDB(**result)


@DM.acqure_connection()
async def delete(
    master_id: int,
    user_profile_id: int,
    conn: Connection = None,
) -> ApprovalInDB:
    result = await conn.fetchrow(
        # 'with profile as ( '
        #     'select '
        #         ' * '
        #     'from '
        #         'user_profile  '
        #     'where '
        #         'user_profile.real_id = $1 '
        # ') '
        # 'delete from '
        #     'master_approvals '
        # 'where '
        #     'user_profile_id = (select id from profile) '
        #     'and master_id = $2 '
        # 'returning * ',
        # user_real_id,
        # master_id,
        *delete_q(
            'master_approvals',
            master_id=master_id,
            user_profile_id=user_profile_id,
        )
    )
    if not result:
        return result
    return ApprovalInDB(**result)


@DM.acqure_connection()
async def get_request(
    # user_real_id: int,
    master_id: int,
    conn: Connection = None,
) -> ApprovalRequestInDB:
    result = await conn.fetchrow(
        # 'with profile as ( '
        #     'select '
        #         'master.id as master_id '
        #     'from '
        #         'user_profile  '
        #     'left join '
        #         'master '
        #     'on '
        #         'master.user_profile_id = user_profile.id '
        #     'where '
        #         'user_profile.real_id = $1 '
        # ') '
        # 'select '
        #     '* '
        # 'from '
        #     'master_approve_request '
        # 'where '
        #     'master_id = (select master_id from profile) ',
        # user_real_id,
        *select_q(
            'master_approve_request',
            master_id=master_id,
        )
    )
    if not result:
        return result
    return ApprovalRequestInDB(**result)


@DM.acqure_connection()
async def create_request(
    # user_real_id: int,
    master_id: int,
    conn: Connection = None,
) -> ApprovalRequestInDB:
    result = await conn.fetchrow(
        # 'with profile as ( '
        #     'select '
        #         'master.id as master_id '
        #     'from '
        #         'user_profile  '
        #     'left join '
        #         'master '
        #     'on '
        #         'master.user_profile_id = user_profile.id '
        #     'where '
        #         'user_profile.real_id = $1 '
        # ') '
        # 'insert into master_approve_request '
        #     # '(master_id ) '
        # '(select * from profile)'
        # 'returning * ',
        # user_real_id,
        *insert_q(
            {"master_id": master_id},
            'master_approve_request',
        )
    )
    if not result:
        return result
    return ApprovalRequestInDB(**result)


@DM.acqure_connection()
async def delete_request(
    master_id: int,
    # user_real_id: int,
    conn: Connection = None,
) -> ApprovalRequestInDB:
    result = await conn.fetchrow(
        # 'with profile as ( '
        #     'select '
        #         'master.id as master_id '
        #     'from '
        #         'user_profile  '
        #     'left join '
        #         'master '
        #     'on '
        #         'master.user_profile_id = user_profile.id '
        #     'where '
        #         'user_profile.real_id = $1 '
        # ') '
        # 'delete from master_approve_request '
        #     # '(master_id ) '
        # 'where '
        #     'master_id = (select master_id from profile) '
        # 'returning * ',
        # user_real_id,
        *delete_q(
            'master_approve_request',
            master_id=master_id,
        )
    )
    if not result:
        return result
    return ApprovalRequestInDB(**result)


@DM.acqure_connection()
async def update_request(
    master_id: int,
    request: ApprovalRequestUpdateByAdmin,
    conn: Connection = None,
) -> ApprovalRequestInDB:
    result = await conn.fetchrow(
        *update_q(
            request,
            'master_approve_request',
            master_id=master_id,
        )
    )
    if not result:
        return result
    return ApprovalRequestInDB(**result)
