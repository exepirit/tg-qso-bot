from pyrogram import Client
from dynaconf import settings


app = Client(
    "data",
    api_id=settings.MTPROTO_API.APP_ID,
    api_hash=settings.MTPROTO_API.APP_HASH,
    bot_token=settings.BOT_TOKEN,
)
