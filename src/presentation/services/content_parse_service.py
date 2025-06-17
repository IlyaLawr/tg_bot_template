from abc import ABC, abstractmethod
from typing import Any

from aiogram import Bot
from aiogram.types import Message


class IContentParser(ABC):
    @abstractmethod
    async def extract_content(self, message: Any) -> str | bytes:
        pass


class TelegramMessageParser(IContentParser):
    def __init__(self, bot: Bot):
        self._bot = bot


    async def extract_content(self, message: Message) -> str | bytes:
        if message.photo:
            file = await self._bot.get_file(message.photo[-1].file_id)
            file_io = await self._bot.download_file(file.file_path)
            data: bytes = file_io.read()
            print(type(data))
            return data

        return message.text or message.caption or ''
