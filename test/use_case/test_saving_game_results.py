from pytest import mark

from application.use_case.saving_game_results import SavingGameResultUseCase
from application.use_case.game_action import GameActionUseCase

from domain.entities.user import User
from domain.entities.profile import Profile


@mark.asyncio
async def test_saving_game_results_updates_profile(uow, game_state_cache):
    client_id = 100

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id, taps_statistics=0))

    game_action_uc = GameActionUseCase(game_state=game_state_cache)
    await game_action_uc.execute(client_id)
    await game_action_uc.execute(client_id)

    game = await game_state_cache.get_game(client_id)
    assert len(game.taps) == 2

    saving_uc = SavingGameResultUseCase(game_state=game_state_cache, uow=uow)
    await saving_uc.execute(client_id)

    async with uow as unit:
        profile = await unit.profile_repository.get(client_id)
        assert profile.taps_statistics == 2

    game_after = await game_state_cache.get_game(client_id)
    assert len(game_after.taps) == 0


@mark.asyncio
async def test_saving_game_results_no_profile(uow, game_state_cache):
    client_id = 200

    game_action_uc = GameActionUseCase(game_state=game_state_cache)
    await game_action_uc.execute(client_id)

    saving_uc = SavingGameResultUseCase(game_state=game_state_cache, uow=uow)
    await saving_uc.execute(client_id)

    game = await game_state_cache.get_game(client_id)
    assert len(game.taps) == 0
