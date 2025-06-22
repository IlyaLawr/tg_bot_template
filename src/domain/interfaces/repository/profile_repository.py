from abc import ABC, abstractmethod
from typing import AsyncGenerator

from domain.entities.profile import Profile


class IProfileRepository(ABC):
    @abstractmethod
    async def create(self, profile: Profile) -> None: 
        pass


    @abstractmethod
    async def get(self, id: int) -> Profile | None:
        pass


    @abstractmethod
    async def get_all(self) -> AsyncGenerator[Profile]:
        pass


    @abstractmethod
    async def update(self, profile: Profile) -> bool: 
        pass


    @abstractmethod
    async def delete(self, id: int) -> bool: 
        pass
