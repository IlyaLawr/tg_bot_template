from aiogram.types import Message, CallbackQuery
from aiogram.filters.logic import or_f as Or
from aiogram.filters import Command
from aiogram import Router, F

from application.use_case.game_action import GameActionUseCase

from presentation.services.interaction_state_manager import InteractionStateManager

from presentation.utils.templates import create_result_game
from presentation.utils.keyboards import tap_button
from presentation.utils.filters import StateFilter


def setup_game_handlers(router: Router,
                        use_case_game_action: GameActionUseCase,
                        interaction_state_manager: InteractionStateManager) -> None:

    @router.message(Or(Command('game'), F.text == 'Сыграть в игру'))
    async def command_handler(message: Message) -> None:
        client_id = message.from_user.id

        await interaction_state_manager.update_interaction_state(client_id, 'game')
        await message.answer(create_result_game(),
                             reply_markup=tap_button.as_markup(), 
                             parse_mode='Markdown')


    @router.callback_query(StateFilter('game'), F.data == 'tap')
    async def from_state_handler(callback: CallbackQuery) -> None:
        client_id = callback.from_user.id
        result = await use_case_game_action.execute(client_id)

        await callback.message.edit_text(create_result_game(result), 
                                         reply_markup=tap_button.as_markup(), 
                                         parse_mode='Markdown')
