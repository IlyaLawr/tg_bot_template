from abc import ABC, abstractmethod
from domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> None: 
        pass


    @abstractmethod
    async def get(self, id: int) -> User:
        pass


    @abstractmethod
    async def update(self, profile: User) -> None: 
        pass


    @abstractmethod
    async def delete(self, id: int) -> None: 
        pass
