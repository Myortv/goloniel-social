from typing import List

from asyncpg import Connection

from fastapiplugins.controllers import (
    DatabaseManager as DM,
    select_q,
    update_q,
    delete_q,
    insert_q,
)

from app.schemas.group import (
    ViewGroup,
    GroupInDB,
    # GroupCreate,
    GroupCreateWithMaster,
    GroupUpdate,
    # ViewMaster,
    # MasterCreate,
    # MasterUpdate,
)


@DM.acqure_connection()
async def get_by_request(
    request_id: int,
    conn: Connection = None,
) -> GroupInDB:
    result = await conn.fetchrow(
        'select '
            'playing_group.* '
        'from group_membership_request '
        'left join playing_group '
        'on playing_group.id = group_membership_request.group_id '
        'where group_membership_request.id = $1 ',
        request_id,
    )
    if not result:
        return result
    return GroupInDB(**result)


@DM.acqure_connection()
async def get_by_id(
    group_id: int,
    conn: Connection = None,
) -> ViewGroup:
    result = await conn.fetchrow(*select_q(
        'view_group',
        id=group_id,
    ))
    if not result:
        return result
    return ViewGroup(**result)


@DM.acqure_connection()
async def get_by_user(
    user_profile_id: int,
    conn: Connection = None,
) -> List[GroupInDB]:
    result = await conn.fetch(
        # 'with profile as ( '
        #     'select '
        #         'user_profile.id user_profile_id, '
        #         'master.id master_id '
        #     'from '
        #         'user_profile '
        #     'left join '
        #         'master '
        #     'on master.user_profile_id = user_profile.id '
        #     'where '
        #         'real_id = $1 '
        # 'with related_users as ( '
        #     'select '
        #         'lnk_group_user.group_id  '
        #     'from '
        #         'lnk_group_user '
        #     'where user_profile_id = $1'
        # ') '
        # 'select  '
        #     'playing_group.* '
        # 'from '
        #     'playing_group '
        # 'where '
        #     'playing_group.master_id = (select master_id from profile) '
        #         'or '
        #     'id = (select group_id from related_users) ',
        '( '
        'select '
            'playing_group.* '
        'from lnk_group_user '
        'left join '
            'playing_group '
        'on playing_group.id = lnk_group_user.group_id '
        'where lnk_group_user.user_profile_id = $1 '
        ') '
        'union ('
            'select playing_group.* '
            'from playing_group '
            'left join master '
            'on master.id = playing_group.master_id '
        'where master.user_profile_id = $1 '
        ') ',
        user_profile_id,
    )
    if not result:
        return result
    return [GroupInDB(**row) for row in result]


@DM.acqure_connection()
async def get_by_verobouse(
    real_user_id: int,
    conn: Connection = None,
) -> List[GroupInDB]:
    result = await conn.fetch(
        'with profile as ( '
            'select '
                'user_profile.id user_profile_id, '
                'master.id master_id '
            'from '
                'user_profile '
            'left join '
                'master '
            'on master.user_profile_id = user_profile.id '
            'where '
                'real_id = $1 '
        'with related_users as ( '
            'select '
                'lnk_group_user.group_id  '
            'from '
                'lnk_group_user '
            'where user_profile_id = $1'
        ') '
        'select  '
            'playing_group.* '
        'from '
            'playing_group '
        'where '
            'playing_group.master_id = (select master_id from profile) '
                'or '
            'id = (select group_id from related_users) ',
        real_user_id,
    )
    if not result:
        return result
    return [GroupInDB(**row) for row in result]


@DM.acqure_connection()
async def create(
    group: GroupCreateWithMaster,
    conn: Connection = None,
) -> GroupInDB:
    result = await conn.fetchrow(
        # 'with profile as ( '
        #     'select '
        #         'master.id as master_id '
        #     'from '
        #         'user_profile '
        #     'left join '
        #         'master '
        #     'on master.user_profile_id = user_profile.id '
        #     'where '
        #         'user_profile.real_id = $1 '
        # ') '
        # 'insert into '
        #     'playing_group (master_id, title, description)'
        # '( '
        #     'select profile.*, $2, $3 from profile '
        # ') '
        # 'returning * ',
        # real_user_id,
        # group.title,
        # group.description,
        *insert_q(
            group,
            'playing_group',
        )
    )
    if not result:
        return result
    return GroupInDB(**result)


@DM.acqure_connection()
async def update(
    group: GroupUpdate,
    group_id: int,
    master_id: int,
    conn: Connection = None,
) -> GroupInDB:
    result = await conn.fetchrow(
        *update_q(group, 'playing_group', id=group_id, master_id=master_id)
    )
    if not result:
        return result
    return GroupInDB(**result)


@DM.acqure_connection()
async def delete(
    group_id: int,
    conn: Connection = None,
) -> GroupInDB:
    result = await conn.fetchrow(
        *delete_q('playing_group', id=group_id)
    )
    if not result:
        return result
    return GroupInDB(**result)
