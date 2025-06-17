from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from presentation.utils.templates import help_text


def setup_info_handlers(router: Router) -> None:

    @router.message(Command('info'))
    async def command_handler(message: Message) -> None:
        await message.answer(help_text, parse_mode='Markdown')
