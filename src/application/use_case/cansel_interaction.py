from application.use_case.update_profile import UpdateProfileUseCase
from application.use_case.saving_game_results import SavingGameResultUseCase


class CanselInteractionUseCase:
    def __init__(self, 
                 profile_update_use_case: UpdateProfileUseCase,
                 saving_game_result_use_case: SavingGameResultUseCase) -> None:
        
        self._profile_update_use_case = profile_update_use_case
        self._saving_game_result_use_case = saving_game_result_use_case

        self._types_interaction = {'game': self._saving_game_result_use_case,
                                   'profile': self._profile_update_use_case}


    async def execute(self, client_id: int, type_interaction: str) -> None:
        interaction = self._types_interaction.get(type_interaction)
        if interaction is not None:
            await interaction.execute(client_id)
