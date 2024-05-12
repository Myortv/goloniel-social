# from aio_pika import ExchangeType

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from prometheus_fastapi_instrumentator import Instrumentator


from fastapiplugins.rabbit import RabbitManager

from fastapiplugins.exceptions import prepare_exceptions

from fastapiplugins.controllers import (
    DatabaseManager,
    exceptions as plugins_controllers_exceptions,
)


from app.core.configs import settings, tags_metadata

from app.messages.consumer import user_profile


handled_exceptions = prepare_exceptions(
    plugins_controllers_exceptions
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version='0.0.1',
    docs_url=settings.DOCS_URL,
    openapi_tags=tags_metadata,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    exception_handlers=handled_exceptions,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


from app.api.v1 import (
    master,
    user_profile,
    master_rating,
    master_approval,
    group,
    # group_membership,
    group_message,
)
from app.api.v1.private import (
    group_membership as private_group_membersip,
    group_join_request as private_group_join_request,
)

app.include_router(
    master.api,
    prefix=settings.API_V1_STR + '/master',
    tags=["Master"]
)

app.include_router(
    user_profile.api,
    prefix=settings.API_V1_STR + '/user_profile',
    tags=["User Profile"]
)

app.include_router(
    master_rating.api,
    prefix=settings.API_V1_STR + '/master-rating',
    tags=["Master Rating"]
)
app.include_router(
    master_approval.api,
    prefix=settings.API_V1_STR + '/master-approval',
    tags=["Master Approval"]
)
app.include_router(
    group.api,
    prefix=settings.API_V1_STR + '/group',
    tags=["Group"]
)
# app.include_router(
#     group_membership.api,
#     prefix=settings.API_V1_STR + '/group-membership',
#     tags=["Group Membership"]
# )
app.include_router(
    private_group_join_request.api,
    prefix=settings.API_V1_STR + '/private/group-join-request',
    tags=["Private group join request"]
)
app.include_router(
    private_group_membersip.api,
    prefix=settings.API_V1_STR + '/private/group-membership',
    tags=["Private group membership"]
)
# app.include_router(
#     integrations.api,
#     prefix=settings.API_V1_STR + '/integrations',
#     tags=["Integrations"]
# )

instrumentator = Instrumentator().instrument(app)


@app.on_event('startup')
async def startup():
    await DatabaseManager.start(
        settings.POSTGRES_DB,
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
    )
    await RabbitManager.start(
        settings.RABBITMQ_HOST,
        settings.RABBITMQ_PORT,
        settings.RABBITMQ_USER,
        settings.RABBITMQ_PASSWORD,
    )
    await RabbitManager.start_consuming()
    instrumentator.expose(app, include_in_schema=True, should_gzip=True)


@app.on_event('shutdown')
async def shutdown():
    await DatabaseManager.stop()
    await settings.aiohttp_session.close()
