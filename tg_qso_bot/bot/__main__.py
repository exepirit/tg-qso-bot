import logging
from pyrogram import Client, Filters, Message
from dynaconf import settings
from tg_qso_bot.qso_sources.hamlog import HamlogQsoSource
from .reply_format import format_qso

HELP_MESSAGE = """
Синтаксис команды: `/qso <позывной>`.
Бот покажет последние 10 связей с данным позывным.
"""

logging.basicConfig(format="%(asctime)s - [%(levelname)s] - %(message)s", level=logging.WARN)
app = Client(
    ":memory:",
    api_id=settings.MTPROTO_API.APP_ID,
    api_hash=settings.MTPROTO_API.APP_HASH,
    bot_token=settings.BOT_TOKEN,
)


@app.on_message(Filters.command("qso"))
def request_qso(client: Client, message: Message):
    if len(message.command) < 2:
        message.reply_text(HELP_MESSAGE)
        return
    callsign = message.command[1].upper()
    hamlog = HamlogQsoSource()
    qso_list = hamlog.get_qso_list(callsign, limit=10)
    header = f"Последние {len(qso_list)} связей с {callsign}\n"
    table = "\n".join(format_qso(q) for q in qso_list)
    client.send_message(
        message.chat.id,
        f"{header}```{table}```",
        parse_mode="markdown",
        reply_to_message_id=message.message_id
    )


if __name__ == "__main__":
    app.run()
