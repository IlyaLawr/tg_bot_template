from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces.repository.user_repository import IUserRepository
from domain.entities.user import User

from infrastructure.database.models import UserModel


class SQLUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession | None = None):
        self._session = session


    async def create(self, user: User) -> None:
        user_model = UserModel(client_id=user.client_id,
                               username=user.username,
                               access=user.access)
        self._session.add(user_model)


    async def get(self, id: int) -> User | None:
        user_model = await self._session.get(UserModel, id)

        if user_model:
            return User(client_id=user_model.client_id,
                        username=user_model.username,
                        access=user_model.access)


    async def update(self, user_update: User) -> bool:
        existing_model = await self._session.get(UserModel, user_update.client_id)
        if not existing_model:
            return False

        existing_model.username = user_update.username
        existing_model.access = user_update.access

        await self._session.flush([existing_model])
        return True


    async def delete(self, id: int) -> bool:
        user_model = await self._session.get(UserModel, id)
        if user_model:
            await self._session.delete(user_model)
            return True

        return False
