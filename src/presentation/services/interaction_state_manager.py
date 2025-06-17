from application.use_case.cansel_interaction import CanselInteractionUseCase
from presentation.services.ui_state_service import UIStateServiceInterface


class InteractionStateManager:
    def __init__(self,
                 ui_state_service: UIStateServiceInterface,
                 cancel_interaction_use_case: CanselInteractionUseCase) -> None:

        self._ui_state_service = ui_state_service
        self._cancel_interaction_use_case = cancel_interaction_use_case


    async def update_interaction_state(self, client_id: int, new_state: str) -> None:
        current_state = await self._ui_state_service.get(client_id)

        if current_state is not None:
            await self._cancel_interaction_use_case.execute(client_id, current_state)

        await self._ui_state_service.set(client_id, new_state)


    async def cancel_interaction_state(self, client_id: int) -> None:
        current_state = await self._ui_state_service.get(client_id)
        if current_state is not None:
            await self._cancel_interaction_use_case.execute(client_id, current_state)
            await self._ui_state_service.clear(client_id)
