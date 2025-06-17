from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from presentation.services.interaction_state_manager import InteractionStateManager
from presentation.utils.keyboards import menu_keyboard
from presentation.utils.templates import menu_text


def setup_menu_handlers(router: Router,
                        interaction_state_manager: InteractionStateManager) -> None:

    @router.message(Command('menu'))
    async def command_handler(message: Message) -> None:
        client_id = message.from_user.id

        await interaction_state_manager.cancel_interaction_state(client_id)
        await message.answer(menu_text, reply_markup=menu_keyboard, parse_mode='Markdown')
