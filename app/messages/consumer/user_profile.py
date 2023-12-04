import logging

from fastapiplugins.rabbit import RabbitManager

from app.controllers import user_profile as user_profile_controller


@RabbitManager.subscribe('user_events', 'created')
async def consume_user_created(message: dict):
    try:
        await user_profile_controller.save(
            message['id']
        )
    except Exception as e:
        logging.exception(e)


@RabbitManager.subscribe('user_events', 'deleted')
async def consume_user_deleted(message: dict):
    try:
        await user_profile_controller.delete(
            message['id']
        )
    except Exception as e:
        logging.exception(e)
