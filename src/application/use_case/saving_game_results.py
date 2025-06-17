from domain.interfaces.state_cache.game_state_cache import IGameStateCache
from domain.interfaces.unit_of_work import IUnitOfWork
from domain.entities.profile import Profile
from domain.entities.game import Game


class SavingGameResultUseCase:
    def __init__(self, 
                 game_state: IGameStateCache,
                 uow: IUnitOfWork):

        self._state = game_state
        self._uow = uow


    async def execute(self, client_id: int) -> None:
        game_id = client_id
        game: Game = await self._state.get_game(game_id)
        if not game:
            return

        async with self._uow as uow:
            user_profile: Profile = await uow.profile_repository.get(client_id)

            if user_profile is None:
                return

            result = game.result()
            user_profile.taps_statistics += result
            await uow.profile_repository.update(user_profile)

        await self._state.clear_game(game_id)
