from contextlib import AbstractAsyncContextManager
from abc import abstractmethod
from types import TracebackType
from typing import Type

from domain.interfaces.repository.user_repository import IUserRepository
from domain.interfaces.repository.profile_repository import IProfileRepository


class IUnitOfWork(AbstractAsyncContextManager['IUnitOfWork']):
    """
    Интерфейс Unit of Work, предоставляющий асинхронный контекст
    для работы с транзакцией и репозиториями.
    """

    user_repository: IUserRepository
    profile_repository: IProfileRepository


    @abstractmethod
    async def __aenter__(self) -> 'IUnitOfWork':
        """
        Открывает сессию и начинает транзакцию.
        Должен инициализировать:
          - сессию, которая будет передана в репозитории
          - self.user_repository
          - self.profile_repository
        """
        pass


    @abstractmethod
    async def __aexit__(self,
                        exc_type: Type[BaseException] | None,
                        exc: BaseException | None,
                        tb: TracebackType | None) -> None:
        """
        Закрывает сессию и завершает транзакцию.
        При возникновении исключения (exc_type != None) — откатить,
        иначе — зафиксировать, и закрыть сессию.
        """
        pass


    @abstractmethod
    async def commit(self) -> None:
        """
        Явно зафиксировать текущую транзакцию.
        """
        pass


    @abstractmethod
    async def rollback(self) -> None:
        """
        Явно откатить текущую транзакцию.
        """
        pass
