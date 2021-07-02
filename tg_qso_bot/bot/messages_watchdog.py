import asyncio
import pyrogram
from pyrogram.types import Message, Chat
from typing import Awaitable, Callable, List
from .messages_log import MessagesLog

Callback = Callable[["pyrogram.Client", List[Message]], Awaitable]


class MessagesWatchdog:
    """ Watches on logged messages and emit event if they are deleted. """

    def __init__(self, client: "pyrogram.Client", log: MessagesLog):
        self._client = client
        self._log = log
        self._delete_messages_handlers: List[Callback] = []

    def add_delete_messages_handler(self, callback: Callback):
        """ Add handler for delete messages events. """
        self._delete_messages_handlers.append(callback)

    def on_delete_messages(self):
        """ Same as add_delete_messages_handler. """
        def wrapper(fn: Callback) -> Callback:
            self.add_delete_messages_handler(fn)
            return fn
        return wrapper

    async def glance(self):
        deleted_messages: List[Message] = []
        for record in self._log:
            call_message = await self._client.get_messages(record.chat_id, record.message_id)
            if isinstance(call_message, list):
                call_message = call_message[0]
            if call_message.empty:
                call_message.chat = Chat(id=record.chat_id, type="")
                deleted_messages.append(call_message)
        if len(deleted_messages) > 0:
            await self._emit_deleted_messages(deleted_messages)

    async def _emit_deleted_messages(self, messages: List[Message]):
        for handler in self._delete_messages_handlers:
            await handler(self._client, messages)

    async def run(self):
        while True:
            await self.glance()
            await asyncio.sleep(30)
    
