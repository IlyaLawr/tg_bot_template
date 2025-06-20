from domain.interfaces.state_cache.profile_filling_state_cache import IProfileFillingStateCache
from domain.interfaces.photo_storage_service import IPhotoStorageService
from domain.interfaces.unit_of_work import IUnitOfWork
from domain.entities.profile import Profile


class UpdateProfileUseCase:
    def __init__(self,
                 state_cache: IProfileFillingStateCache,
                 photo_storage_service: IPhotoStorageService,
                 uow: IUnitOfWork):

        self._state_cache = state_cache
        self._photo_storage_service = photo_storage_service
        self._uow = uow


    async def execute(self, client_id) -> bool:
        updates = await self._state_cache.get_profile_updates(client_id)
        if not updates:
            return False

        async with self._uow as uow:
            profile: Profile = await uow.profile_repository.get(client_id)

            for field_name, value in updates.items():
                if hasattr(profile, field_name):
                    if isinstance(value, bytes):
                        value = await self._photo_storage_service.save(client_id, value)
                    setattr(profile, field_name, value)

            await uow.profile_repository.update(profile)

        await self._state_cache.clear(client_id)
        return True
