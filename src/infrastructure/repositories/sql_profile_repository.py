from typing import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces.repository.profile_repository import IProfileRepository
from domain.entities.profile import Profile

from infrastructure.database.models import ProfileModel


class SQLProfileRepository(IProfileRepository):
    def __init__(self, session: AsyncSession | None = None) -> None:
        self._session = session


    async def create(self, profile: Profile) -> None:
        profile_model = ProfileModel(client_id=profile.client_id,
                                     name=profile.name,
                                     taps_statistics=profile.taps_statistics,
                                     about=profile.about,
                                     photo=profile.photo)
        self._session.add(profile_model)


    async def get(self, id: int) -> Profile | None:
        profile_model = await self._session.get(ProfileModel, id)

        if profile_model:
            return Profile(client_id=profile_model.client_id,
                           name=profile_model.name,
                           registration_date=profile_model.registration_date,
                           taps_statistics=profile_model.taps_statistics,
                           about=profile_model.about,
                           photo=profile_model.photo)
        

    async def get_all(self) -> AsyncGenerator[Profile]:

        stmt = select(ProfileModel)

        async for profile_model in await self._session.stream_scalars(stmt):
            yield Profile(client_id=profile_model.client_id,
                          name=profile_model.name,
                          registration_date=profile_model.registration_date,
                          taps_statistics=profile_model.taps_statistics,
                          about=profile_model.about,
                          photo=profile_model.photo)


    async def update(self, profile_update: Profile) -> bool:
        existing_model = await self._session.get(ProfileModel, profile_update.client_id)
        if not existing_model:
            return False

        existing_model.name = profile_update.name
        existing_model.about = profile_update.about
        existing_model.photo = profile_update.photo
        existing_model.taps_statistics = profile_update.taps_statistics

        await self._session.flush([existing_model])
        return True


    async def delete(self, id: int) -> bool:
        profile_model = await self._session.get(ProfileModel, id)
        if profile_model:
            await self._session.delete(profile_model)
            return True

        return False
