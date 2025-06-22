from pathlib import Path
from pytest import mark

from application.use_case.cansel_interaction import CanselInteractionUseCase
from application.use_case.update_profile import UpdateProfileUseCase
from application.use_case.saving_game_results import SavingGameResultUseCase
from application.use_case.game_action import GameActionUseCase

from domain.entities.user import User
from domain.entities.profile import Profile


@mark.asyncio
async def test_cancel_interaction_game_type_updates_profile(uow, game_state_cache, profile_state_cache, photo_storage):
    client_id = 100

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id))

    game_action_uc = GameActionUseCase(game_state=game_state_cache)
    result1 = await game_action_uc.execute(client_id)
    result2 = await game_action_uc.execute(client_id)
    assert result1 == 1 and result2 == 2

    game = await game_state_cache.get_game(client_id)
    assert len(game.taps) == 2

    update_profile_uc = UpdateProfileUseCase(profile_state_cache, photo_storage, uow)
    saving_game_uc = SavingGameResultUseCase(game_state_cache, uow)
    cancel_uc = CanselInteractionUseCase(update_profile_uc, saving_game_uc)
    await cancel_uc.execute(client_id, type_interaction='game')

    async with uow as unit:
        profile = await unit.profile_repository.get(client_id)
        assert profile.taps_statistics == 2

    game_after = await game_state_cache.get_game(client_id)
    assert len(game_after.taps) == 0


@mark.asyncio
async def test_cancel_interaction_profile_type_updates_profile_and_clears_state(uow, game_state_cache, profile_state_cache, photo_storage):
    client_id = 200

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id, 
                                                     name='', 
                                                     about='', 
                                                     photo=''))

    await profile_state_cache.set_field_answer(client_id, 'name', 'Петро')
    await profile_state_cache.set_field_answer(client_id, 'about', 'Сливаю мид за пуджа')

    fake_photo = b'\xff\xd8\xff'
    await profile_state_cache.set_field_answer(client_id, 'photo', fake_photo)

 
    update_profile_uc = UpdateProfileUseCase(profile_state_cache, photo_storage, uow)
    saving_game_uc = SavingGameResultUseCase(game_state_cache, uow)
    cancel_uc = CanselInteractionUseCase(update_profile_uc, saving_game_uc)
    await cancel_uc.execute(client_id, type_interaction='profile')

 
    async with uow as unit:
        profile = await unit.profile_repository.get(client_id)
        assert profile.name == 'Петро'
        assert profile.about == 'Сливаю мид за пуджа'
        assert profile.photo != ''
        assert Path(profile.photo).exists()
    
        with open(profile.photo, 'rb') as f:
            content = f.read()
        assert content == fake_photo

    updates = await profile_state_cache.get_profile_updates(client_id)
    assert updates == {}


@mark.asyncio
async def test_cancel_interaction_invalid_type_does_nothing(uow, game_state_cache, profile_state_cache, photo_storage):
    client_id = 300

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id))

    async with uow as unit:
        profile = await unit.profile_repository.get(client_id)
        assert profile.taps_statistics == 0

    update_profile_uc = UpdateProfileUseCase(profile_state_cache, photo_storage, uow)
    saving_game_uc = SavingGameResultUseCase(game_state_cache, uow)
    cancel_uc = CanselInteractionUseCase(update_profile_uc, saving_game_uc)
    await cancel_uc.execute(client_id, type_interaction='hamster_combat')

    async with uow as unit:
        profile = await unit.profile_repository.get(client_id)
        assert profile.taps_statistics == 0
        assert profile.name == f'Игрок {client_id}'
        assert profile.about == 'Обычный игрок'
