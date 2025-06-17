from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter

from presentation.services.ui_state_service import UIStateServiceInterface


Update = Message | CallbackQuery

class StateFilter(BaseFilter):
    def __init__(self, state: str) -> None:
        self.state = state


    async def __call__(self, 
                       update: Update, 
                       ui_state_service: UIStateServiceInterface) -> bool:
        
        client_id = update.from_user.id
        current_state = await ui_state_service.get(client_id)
        return current_state == self.state
