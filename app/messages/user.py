from ujson import dumps

import aio_pika
from aio_pika import Channel, Exchange, ExchangeType, Message

from app.schemas.user import UserInDBProtected

from fastapiplugins.rabbit import RabbitManager


@RabbitManager.acquire_channel('user_events', ExchangeType.DIRECT)
async def emit_created(
    user: UserInDBProtected,
    channel: Channel = None,
    exchange: Exchange = None,
) -> bool:
    message = await exchange.publish(
        Message(
            user.model_dump_json().encode(),
        ),
        routing_key='created'
    )
    if message:
        return True
    return False


@RabbitManager.acquire_channel('user_events', ExchangeType.DIRECT)
async def emit_deleted(
    user: UserInDBProtected,
    channel: Channel = None,
    exchange: Exchange = None,
):
    message = await exchange.publish(
        Message(
            user.model_dump_json().encode(),
        ),
        routing_key='deleted'
    )
    if message:
        return True
    return False
