import sentry_sdk
from pyrogram import Client
from pyrogram.types import Message

_ERROR_MESSAGE = "😟 Something went wrong.\nAccident ID: {accident_id}"


def _set_event_context(scope: sentry_sdk.Scope, message: Message):
    user = message.from_user
    display_name = user.first_name + f" {user.last_name}" if user.last_name else ""
    scope.set_user(
        {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "display_name": display_name,
        }
    )
    scope.set_context("message", message.__dict__)


def handle_errors(fn):
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        with sentry_sdk.push_scope() as scope:
            _set_event_context(scope, message)
            try:
                await fn(client, message, *args, **kwargs)
            except Exception as e:
                accident_id = sentry_sdk.capture_exception(e, scope=scope)
                await client.send_message(
                    message.chat.id, _ERROR_MESSAGE.format(accident_id=accident_id)
                )

    return wrapper
