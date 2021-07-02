import logging
import pyrogram
from typing import List
from tg_qso_bot.bot import messages_log
from tg_qso_bot.bot.app import watchdog, log

_logger = logging.getLogger("bot")


async def delete_reply(client: "pyrogram.Client", record: "messages_log.LogRecord"):
    await client.delete_messages(record.chat_id, record.reply_id)
    _logger.info("Deleted reply message #%d in chat #%d", record.reply_id, record.chat_id)


@watchdog.on_delete_messages()
async def on_delete_reply(client: "pyrogram.Client", deleted_messages: List["pyrogram.types.Message"]):
    for deleted_message in deleted_messages:
        if deleted_message.chat is None:
            _logger.warning("Message #%d deleted in unknown chat", deleted_message.message_id)
            continue
        for record in log:
            if deleted_message.message_id == record.message_id and deleted_message.chat.id == record.chat_id:
                await delete_reply(client, record)
                log.delete_record(record.chat_id, record.message_id)


