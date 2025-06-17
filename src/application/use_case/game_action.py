from domain.interfaces.state_cache.game_state_cache import IGameStateCache
from domain.entities.game import Game
from domain.entities.tap import Tap


class GameActionUseCase:
    def __init__(self, game_state: IGameStateCache):
        self._state = game_state


    async def execute(self, client_id: int) -> int:
        game_id = client_id
        tap: Tap = Tap()

        game: Game = await self._state.get_game(game_id)      
        game.add_tap(tap)

        await self._state.add_tap(game_id, tap)

        return game.result()
