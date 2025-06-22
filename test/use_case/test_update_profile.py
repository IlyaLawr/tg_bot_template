from pytest import mark

from application.use_case.update_profile import UpdateProfileUseCase

from domain.entities.user import User
from domain.entities.profile import Profile


@mark.asyncio
async def test_update_profile_with_updates(uow, profile_state_cache, photo_storage):
    client_id = 100

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id))

    await profile_state_cache.set_field_answer(client_id, 'name', 'Илон Макс')
    await profile_state_cache.set_field_answer(client_id, 'about', 'Релоцировался в Россию из за соры с Трампом..')
    fake_photo = b'\xff\xd8\xff'
    await profile_state_cache.set_field_answer(client_id, 'photo', fake_photo)

    update_uc = UpdateProfileUseCase(state_cache=profile_state_cache, photo_storage_service=photo_storage, uow=uow)
    await update_uc.execute(client_id)

    async with uow as unit:
        profile = await unit.profile_repository.get(client_id)
        assert profile.name == 'Илон Макс'
        assert profile.about == 'Релоцировался в Россию из за соры с Трампом..'
        assert profile.photo != ''
   
        with open(profile.photo, 'rb') as f:
            content = f.read()
        assert content == fake_photo

    updates = await profile_state_cache.get_profile_updates(client_id)
    assert updates == {}


@mark.asyncio
async def test_update_profile_no_updates(uow, profile_state_cache, photo_storage):
    client_id = 200

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id))

    update_uc = UpdateProfileUseCase(state_cache=profile_state_cache, photo_storage_service=photo_storage, uow=uow)
    await update_uc.execute(client_id)

    async with uow as unit:
        profile = await unit.profile_repository.get(client_id)

        assert profile.name == 'Игрок 200'
        assert profile.about == 'Обычный игрок'
        assert profile.photo == ''
