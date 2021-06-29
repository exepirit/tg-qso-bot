import logging
from typing import List
from pyrogram import Client
from pyrogram.types import Message
from tg_qso_bot.bot.app import app, log
from tg_qso_bot.bot.messages_log import MessagesLog

_logger = logging.getLogger("bot")


class GarbageReplysCollector:
    """ Collects and delete dangling bot replys without parent message. """

    def __init__(self, client: Client, log: MessagesLog) -> None:
        self._client = client
        self._log = log

    async def delete_garbage_replys_for(self, message_id: int):
        """ Delete dangling bot replys for message with ID `message_id`. """
        if not self._log.has_reply(message_id):
            return

        for reply in self._log.iter_replys(message_id):
            await self._delete_reply_in_chat(reply.chat_id, reply.reply_id)

    async def _delete_reply_in_chat(self, chat_id: int, reply_id: int):
        reply_message = await self._client.get_messages(chat_id, reply_id)
        if not isinstance(reply_message, Message):
            return
        if reply_message.reply_to_message.empty:
            await self._client.delete_messages(chat_id, reply_id)
            _logger.info("Deleted reply message #%d", reply_id)


@app.on_deleted_messages()
async def delete_messages(client: Client, messages: List[Message]):
    collector = GarbageReplysCollector(client, log)
    for message in messages:
        await collector.delete_garbage_replys_for(message.message_id)

