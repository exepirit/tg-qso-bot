from typing import List, Iterator
from dataclasses import dataclass
from pyrogram.types import Message


@dataclass
class LogRecord:
    chat_id: int
    message_id: int
    reply_id: int


class MessagesLog:
    """ Log for outcoming reply messages for futher deletion handling. """

    def __init__(self, buffer_size: int = 200) -> None:
        self._buffer: List[LogRecord] = []
        self._buffer_max_size = buffer_size

    def register_reply(self, to_message: Message, reply: Message):
        """ Register bot reply in log. """
        record = LogRecord(
            chat_id=to_message.chat.id,
            message_id=to_message.message_id,
            reply_id=reply.message_id,
        )
        self._put_record(record)

    def has_reply(self, message_id: int) -> bool:
        """ Returns True if provided message has logged reply. """
        return any(
            r.message_id == message_id
            for r in self._buffer
        )

    def iter_replys(self, message_id: int) -> Iterator[LogRecord]:
        """ Returns log records, that are reply for provided message. """
        for r in self._buffer:
            if r.message_id == message_id:
                yield r

    def _put_record(self, record: LogRecord) -> int:
        if len(self._buffer) > self._buffer_max_size:
            self._buffer.pop(0)
        self._buffer.append(record)
        return len(self._buffer) - 1

