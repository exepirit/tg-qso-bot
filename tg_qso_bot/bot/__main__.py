import logging
import sentry_sdk
from pyrogram import Client, filters
from pyrogram.types import Message
from dynaconf import settings
from tg_qso_bot.qso_sources.hamlog import HamlogQsoSource
from .reply_format import format_qso
from .errors_handling import handle_errors

HELP_MESSAGE = """
Синтаксис команды: `/qso <позывной>`.
Бот покажет последние 10 связей с данным позывным.
"""

_logger = logging.getLogger("bot")
app = Client(
    "data",
    api_id=settings.MTPROTO_API.APP_ID,
    api_hash=settings.MTPROTO_API.APP_HASH,
    bot_token=settings.BOT_TOKEN,
)


@app.on_message(filters.command("qso"))
@handle_errors
async def request_qso(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(HELP_MESSAGE)
        return
    callsign = message.command[1].upper()
    user_name = (
        message.from_user.first_name + f" {message.from_user.last_name}"
        if message.from_user.last_name
        else ""
    )
    _logger.info(
        'User "%s" (%d) requested QSO for "%s"', user_name, message.from_user.id, callsign,
    )
    hamlog = HamlogQsoSource()
    qso_list = hamlog.get_qso_list(callsign, limit=10)
    header = f"Последние {len(qso_list)} связей с {callsign}\n"
    table = "\n".join(format_qso(q) for q in qso_list)
    await client.send_message(
        message.chat.id,
        f"{header}```{table}```",
        parse_mode="markdown",
        reply_to_message_id=message.message_id,
    )


if __name__ == "__main__":
    sentry_sdk.init()
    app.run()
