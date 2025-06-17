from abc import ABC, abstractmethod
from datetime import datetime

from domain.entities.game import Game
from domain.entities.tap import Tap


class IGameFactory(ABC):
    """Интерфейс фабрики для создания игровых объектов."""
    
    @abstractmethod
    def create_game(self, game_id: int, taps_data: list[dict]) -> Game:
        """Создает объект Game из данных"""
        pass

    @abstractmethod
    def create_tap(self, tap_id: str, timestamp_iso: str) -> Tap:
        """Создает объект Tap из данных"""
        pass


class GameFactory(IGameFactory):
    def create_game(self, game_id: int, taps_data: list[dict]) -> Game | None:
        if not taps_data:
            return Game(id=game_id, taps=[])

        taps = []
        for tap_data in taps_data:
            tap = self.create_tap(tap_data['id'], tap_data['timestamp'])
            taps.append(tap)
        return Game(id=game_id, taps=taps)


    def create_tap(self, tap_id: str, timestamp_iso: str) -> Tap:
        return Tap(id=tap_id, timestamp=datetime.fromisoformat(timestamp_iso))
