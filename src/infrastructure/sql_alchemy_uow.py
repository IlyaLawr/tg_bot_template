from types import TracebackType
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from domain.interfaces.unit_of_work import IUnitOfWork
from domain.interfaces.repository.user_repository import IUserRepository
from domain.interfaces.repository.profile_repository import IProfileRepository


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self,
                 db_url: str,
                 user_repo_cls: Type[IUserRepository],
                 profile_repo_cls: Type[IProfileRepository]):
        
        self._engine = create_async_engine(db_url, future=True, echo=False)
        self._async_session = sessionmaker(self._engine,
                                           class_=AsyncSession,
                                           expire_on_commit=False)

        self._user_repo_cls = user_repo_cls
        self._profile_repo_cls = profile_repo_cls

        self.session: AsyncSession | None = None
        self.user_repository: IUserRepository
        self.profile_repository: IProfileRepository


    async def __aenter__(self) -> 'SqlAlchemyUnitOfWork':
        self.session = self._async_session()
        await self.session.begin()

        self.user_repository = self._user_repo_cls(self.session)
        self.profile_repository = self._profile_repo_cls(self.session)

        return self


    async def __aexit__(self,
                        exc_type: Type[BaseException] | None,
                        exc: BaseException | None,
                        tb: TracebackType | None) -> None:

        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()


    async def commit(self) -> None:
        await self.session.commit()


    async def rollback(self) -> None:
        await self.session.rollback()
