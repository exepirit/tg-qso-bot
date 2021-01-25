import logging
from pyrogram import Client, Filters, Message
from dynaconf import settings
from tg_qso_bot.qso_sources.hamlog import HamlogQsoSource
from tg_qso_bot.utils.logging import create_logger
from .reply_format import format_qso

HELP_MESSAGE = """
Синтаксис команды: `/qso <позывной>`.
Бот покажет последние 10 связей с данным позывным.
"""

_logger = create_logger("bot")
app = Client(
    "data",
    api_id=settings.MTPROTO_API.APP_ID,
    api_hash=settings.MTPROTO_API.APP_HASH,
    bot_token=settings.BOT_TOKEN,
)


@app.on_message(Filters.command(["qso", f"qso@{settings.BOT_NAME}"]))
def request_qso(client: Client, message: Message):
    if len(message.command) < 2:
        message.reply_text(HELP_MESSAGE)
        return
    callsign = message.command[1].upper()
    _logger.info(
        'User \"%s %s\" (%d) requested QSO for "%s"',
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.id,
        callsign,
    )
    hamlog = HamlogQsoSource()
    qso_list = hamlog.get_qso_list(callsign, limit=10)
    header = f"Последние {len(qso_list)} связей с {callsign}\n"
    table = "\n".join(format_qso(q) for q in qso_list)
    client.send_message(
        message.chat.id,
        f"{header}```{table}```",
        parse_mode="markdown",
        reply_to_message_id=message.message_id,
    )


if __name__ == "__main__":
    app.run()
