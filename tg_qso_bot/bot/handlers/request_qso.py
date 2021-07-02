import logging
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message
from dynaconf import settings
from tg_qso_bot.qso_sources.hamlog import HamlogQsoSource
from tg_qso_bot.bot.errors_handling import handle_errors
from tg_qso_bot.bot.app import app, log
from tg_qso_bot.models import Qso

HELP_MESSAGE = """
Синтаксис команды: `/qso <позывной>`.
Бот покажет последние 10 связей с данным позывным.
"""

_logger = logging.getLogger("bot")


def format_qso(q: Qso) -> str:
    return f"{q.call_sign_2:<6} {q.date.strftime('%d.%m.%y'):<8} {q.band:<3} {q.mode}"


def _command_filter(cmd: str, delimiter: str = "@") -> Callable:
    return filters.command([cmd, cmd + delimiter + str(settings.BOT_NAME)])


@app.on_message(_command_filter("qso"))
@handle_errors()
async def request_qso(client: Client, message: Message):
    if len(message.command) < 2:
        reply_message = await message.reply_text(HELP_MESSAGE)
        log.register_reply(message, reply_message)
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
    reply_message = await client.send_message(
        message.chat.id,
        f"{header}```{table}```",
        parse_mode="markdown",
        reply_to_message_id=message.message_id,
    )
    log.register_reply(message, reply_message)
