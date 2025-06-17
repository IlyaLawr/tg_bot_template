from abc import ABC, abstractmethod

from domain.entities.game import Game
from domain.entities.tap import Tap


class IGameStateCache(ABC):
    @abstractmethod
    async def get_game(self, game_id: int) -> Game:
        pass


    @abstractmethod
    async def add_tap(self, game_id: int, tap: Tap) -> None:
        pass


    @abstractmethod
    async def clear_game(self, game_id: int) -> None:
        pass
