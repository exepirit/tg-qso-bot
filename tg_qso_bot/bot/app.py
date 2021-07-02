from pyrogram import Client
from dynaconf import settings
from .messages_log import MessagesLog
from .messages_watchdog import MessagesWatchdog


app = Client(
    "data",
    api_id=str(settings.MTPROTO_API.APP_ID),
    api_hash=str(settings.MTPROTO_API.APP_HASH),
    bot_token=str(settings.BOT_TOKEN),
)
log = MessagesLog()
watchdog = MessagesWatchdog(app, log)
