from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.logic import or_f as Or
from aiogram.types import Message, ReplyKeyboardRemove

from application.use_case.filling_profile import FillingProfileUseCase
from application.dto import FormUserRequest, FormUserResponse

from presentation.services.interaction_state_manager import InteractionStateManager
from presentation.services.content_parse_service import IContentParser
from presentation.utils.keyboards import exit_filling_keyboard, menu_keyboard
from presentation.utils.templates import menu_text
from presentation.utils.filters import StateFilter


def setup_filling_profile_handlers(router: Router,
                                   interaction_state_manager: InteractionStateManager,
                                   content_parser: IContentParser,
                                   use_case_filling_profile: FillingProfileUseCase) -> None:

    @router.message(Or(Command('set_profile'), F.text == 'Изменить профиль'))
    async def command_handler(message: Message) -> None:
        client_id = message.from_user.id
        await interaction_state_manager.update_interaction_state(client_id, 'profile')

        request = FormUserRequest(client_id=client_id, content='')
        response: FormUserResponse = await use_case_filling_profile.execute(request)

        await message.answer(response.message, reply_markup=exit_filling_keyboard)


    @router.message(StateFilter('profile'), F.text == 'Отмена')
    async def exit_handler(message: Message) -> None:
        client_id = message.from_user.id
        await interaction_state_manager.cancel_interaction_state(client_id)
        await message.answer(menu_text, reply_markup=menu_keyboard, parse_mode='Markdown')


    @router.message(StateFilter('profile'))
    async def from_state_handler(message: Message) -> None:
        client_id = message.from_user.id

        content = await content_parser.extract_content(message)
        request = FormUserRequest(client_id=client_id, content=content)
        response: FormUserResponse = await use_case_filling_profile.execute(request)

        if response.success:
            if not response.complete:
                await message.answer(response.message, reply_markup=exit_filling_keyboard)
            else:
                await message.answer(response.message, reply_markup=ReplyKeyboardRemove())
                await interaction_state_manager.cancel_interaction_state(client_id)
        else:
            await message.answer(response.error, reply_markup=exit_filling_keyboard)
