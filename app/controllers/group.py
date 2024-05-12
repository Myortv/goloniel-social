from typing import List, Optional, Tuple, Any


from asyncpg import Connection


from fastapiplugins.controllers import (
    DatabaseManager as DM,
    select_q,
    update_q,
    delete_q,
    insert_q,
)

from app.schemas.group import (
    # ViewGroup,
    GroupInDB,
    # GroupCreate,
    GroupCreateWithMaster,
    GroupUpdate,
    # ViewMaster,
    # MasterCreate,
    # MasterUpdate,
)

from app.utils.controllers import create_optional_filters
# move to fastapi plugins in future
# (update existing fastapi plugins code to use it)


# @DM.acqure_connection()
# async def get_by_master_title(
#     master_id: int,
#     group_title: str,
#     conn: Connection = None,
# ) -> GroupInDB:
#     title_str = ""
#     # title_str = "and regexp_like(title, $2, 'i')"
#     title_str = "and title like $2"
#     group_title = f"%{group_title}%"
#     result = await conn.fetch(
#     #     'select '
#     #         'view_group.* '
#     #     'from view_group '
#     #     'where master_id = $1 '
#     #     f'{title_str} '
#     #     'order by created_at ',
#     #     master_id,
#     #     group_title,
#         select_q(
#         'squad',
#         ['crated at', 'group_title'],
#         master_id=master_id,
#     )
#     )
#     if not result:
#         return result
#     return [GroupInDB(**row) for row in result]

# @DM.acqure_connection()
# async def get_titles_complete(
#     conn: Connection = None,
# ) -> List[dict]:
#     titles = await conn.fetch(
#         """
#         select title from squad
#         """
#     )


@DM.acqure_connection()
async def page(
    offset: int,
    limit: int,
    conn: Connection = None,
) -> List[GroupInDB]:
    page = await conn.fetch(
        """
            select * from squad
            order by is_full nulls last
            limit $1
            offset $2
        """,
        limit,
        offset,
    )
    if page:
        return [GroupInDB(**row) for row in page]


@DM.acqure_connection()
async def page_by_user_id(
    user_id: int,
    offset: int,
    limit: int,
    conn: Connection = None,
) -> List[GroupInDB]:
    page = await conn.fetch(
        """
            select squad.* from lnk_squad_user
            left join squad
            on squad.id = lnk_squad_user.squad_id
            where
                lnk_squad_user.user_id = $1
            order by is_full nulls last
            limit $2
            offset $3
        """,
        user_id,
        limit,
        offset,
    )
    if page:
        return [GroupInDB(**row) for row in page]


@DM.acqure_connection()
async def page_search(
    master_id: Optional[int],
    search_by: Optional[str],
    offset: int,
    limit: int,
    conn: Connection = None,
) -> List[GroupInDB]:
    filters, args, index = create_optional_filters(
        master_id=master_id,
    )
    if search_by:
        filters.append(f"( title like ${index} or description like ${index} )")
        index += 1
        args.append(
           f'%{search_by}%'
        )
    filter = ""
    if filters or search_by:
        filter = "where "
        filter += ' and '.join(filters)
    result = await conn.fetch(
        f"""
        select * from squad
        {filter}
        order by is_full nulls last,
        created_at desc
        limit ${index} offset ${index+1}
        """,
        *args,
        limit,
        offset,
    )
    if not result:
        return result
    return [GroupInDB(**row) for row in result]


@DM.acqure_connection()
async def get_by_master(
    master_id: int,
    offset: int,
    limit: int,
    conn: Connection = None,
) -> List[GroupInDB]:
    result = await conn.fetch(
        """
        select * from squad
        where master_id = $1
        order by created_at
        limit $2 offset $3
        """,
        master_id,
        limit,
        offset,
    )
    if not result:
        return result
    return [GroupInDB(**row) for row in result]


# @DM.acqure_connection()
# async def get_by_request(
#     request_id: int,
#     conn: Connection = None,
# ) -> GroupInDB:
#     result = await conn.fetchrow(
#         'select '
#             'squad.* '
#         'from group_membership_request '
#         'left join playing_group '
#         'on playing_group.id = group_membership_request.group_id '
#         'where group_membership_request.id = $1 ',
#         request_id,
#     )
#     if not result:
#         return result
#     return GroupInDB(**result)


@DM.acqure_connection()
async def get_by_id(
    group_id: int,
    conn: Connection = None,
) -> GroupInDB:
    result = await conn.fetchrow(*select_q(
        'squad',
        id=group_id,
    ))
    if not result:
        return result
    return GroupInDB(**result)


# @DM.acqure_connection()
# async def get_by_user(
#     user_id: int,
#     conn: Connection = None,
# ) -> List[GroupInDB]:
#     result = await conn.fetch(
#         # 'with profile as ( '
#         #     'select '
#         #         'user_profile.id user_id, '
#         #         'master.id master_id '
#         #     'from '
#         #         'user_profile '
#         #     'left join '
#         #         'master '
#         #     'on master.user_id = user_profile.id '
#         #     'where '
#         #         'real_id = $1 '
#         # 'with related_users as ( '
#         #     'select '
#         #         'lnk_group_user.group_id  '
#         #     'from '
#         #         'lnk_group_user '
#         #     'where user_id = $1'
#         # ') '
#         # 'select  '
#         #     'playing_group.* '
#         # 'from '
#         #     'playing_group '
#         # 'where '
#         #     'playing_group.master_id = (select master_id from profile) '
#         #         'or '
#         #     'id = (select group_id from related_users) ',
#         '( '
#         'select '
#             'playing_group.* '
#         'from lnk_group_user '
#         'left join '
#             'playing_group '
#         'on playing_group.id = lnk_group_user.group_id '
#         'where lnk_group_user.user_id = $1 '
#         ') '
#         'union ('
#             'select playing_group.* '
#             'from playing_group '
#             'left join master '
#             'on master.id = playing_group.master_id '
#         'where master.user_id = $1 '
#         ') ',
#         user_id,
#     )
#     if not result:
#         return result
#     return [GroupInDB(**row) for row in result]


# @DM.acqure_connection()
# async def get_by_verobouse(
#     real_user_id: int,
#     conn: Connection = None,
# ) -> List[GroupInDB]:
#     result = await conn.fetch(
#         'with profile as ( '
#             'select '
#                 'user_profile.id user_id, '
#                 'master.id master_id '
#             'from '
#                 'user_profile '
#             'left join '
#                 'master '
#             'on master.user_id = user_profile.id '
#             'where '
#                 'real_id = $1 '
#         'with related_users as ( '
#             'select '
#                 'lnk_group_user.group_id  '
#             'from '
#                 'lnk_group_user '
#             'where user_id = $1'
#         ') '
#         'select  '
#             'playing_group.* '
#         'from '
#             'playing_group '
#         'where '
#             'playing_group.master_id = (select master_id from profile) '
#                 'or '
#             'id = (select group_id from related_users) ',
#         real_user_id,
#     )
#     if not result:
#         return result
#     return [GroupInDB(**row) for row in result]


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
        #     'on master.user_id = user_profile.id '
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
            'squad',
        )
    )
    if not result:
        return result
    return GroupInDB(**result)


@DM.acqure_connection()
async def update(
    group: GroupUpdate,
    group_id: int,
    conn: Connection = None,
) -> GroupInDB:
    result = await conn.fetchrow(
        *update_q(
            group,
            'squad',
            id=group_id,
        )
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
        *delete_q('squad', id=group_id)
    )
    if not result:
        return result
    return GroupInDB(**result)
