from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from application.use_case.register_user import RegisterUserUseCase
from application.use_case.access_check import AccessCheckUseCase
from application.dto import RegisterUserRequest, RegisterUserResponse, CheckUserResponse

from presentation.services.interaction_state_manager import InteractionStateManager
from presentation.utils.filters import StateFilter


def setup_start_handlers(router: Router,
                         use_case_register_user: RegisterUserUseCase,
                         use_case_access_check: AccessCheckUseCase,
                         interaction_state_manager: InteractionStateManager) -> None:

    @router.message(Command('start'))
    async def command_handler(message: Message) -> None:
        client_id = message.from_user.id

        response: CheckUserResponse = await use_case_access_check.execute(client_id)
        if response.success:
            await message.answer(response.message)
        else:
            await message.answer(response.message)
            await interaction_state_manager.update_interaction_state(client_id, 'register')


    @router.message(StateFilter('register'))
    async def from_state_handler(message: Message) -> None:
        client_id = message.from_user.id

        request = RegisterUserRequest(client_id=client_id,
                                      username=message.from_user.username,
                                      pass_phrase=message.text or '')
        response: RegisterUserResponse = await use_case_register_user.execute(request)

        if response.success:
            await message.answer(response.message)
            await interaction_state_manager.cancel_interaction_state(client_id)
        else:
            await message.answer(response.message)
