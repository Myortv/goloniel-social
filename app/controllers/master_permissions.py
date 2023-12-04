from asyncpg import Connection


from fastapiplugins.controllers import (
    DatabaseManager as DM,
    select_q,
)

from app.schemas.user import (
    ViewMasterInDB,
    ViewMaster,
)


@DM.acqure_connection()
async def get_master(
    real_user_id: int,
    conn: Connection = None,
) -> ViewMaster:
    result = await conn.fetchrow(*select_q(
        'view_master',
        ViewMasterInDB,
        user_real_id=real_user_id,
    ))
    if not result:
        return result
    return ViewMasterInDB(**result)
