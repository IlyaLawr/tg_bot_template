from pytest import mark

from application.use_case.register_user import RegisterUserUseCase
from application.use_case.game_action import GameActionUseCase
from application.dto import RegisterUserRequest


SECRET_PHRASE = 'voicee_forever'


@mark.asyncio
async def test_game_action_adds_taps(uow, game_state_cache):
    client_id = 100

    register_uc = RegisterUserUseCase(pass_phrase=SECRET_PHRASE, uow=uow)
    reg_request = RegisterUserRequest(client_id=client_id,
                                      username=f'user{client_id}',
                                      pass_phrase=SECRET_PHRASE)
    reg_response = await register_uc.execute(reg_request)
    assert reg_response.success is True

    game_action_uc = GameActionUseCase(game_state=game_state_cache)

    result1 = await game_action_uc.execute(client_id)
    assert result1 == 1

    game = await game_state_cache.get_game(client_id)
    assert len(game.taps) == 1

    result2 = await game_action_uc.execute(client_id)
    assert result2 == 2

    game2 = await game_state_cache.get_game(client_id)
    assert len(game2.taps) == 2


@mark.asyncio
async def test_game_action_no_prior_game(uow, game_state_cache):
    client_id = 200

    register_uc = RegisterUserUseCase(pass_phrase=SECRET_PHRASE, uow=uow)
    reg_request = RegisterUserRequest(client_id=client_id,
                                      username=f'user{client_id}',
                                      pass_phrase=SECRET_PHRASE)
    reg_response = await register_uc.execute(reg_request)
    assert reg_response.success is True

    game_action_uc = GameActionUseCase(game_state=game_state_cache)

    result = await game_action_uc.execute(client_id)
    assert result == 1

    game = await game_state_cache.get_game(client_id)
    assert len(game.taps) == 1


@mark.asyncio
async def test_game_action_multiple_clients(uow, game_state_cache):
    client1_id, client2_id = 300, 400

    register_uc = RegisterUserUseCase(pass_phrase=SECRET_PHRASE, uow=uow)
    for client_id in (client1_id, client2_id):
        reg_request = RegisterUserRequest(client_id=client_id,
                                          username=f'user{client_id}',
                                          pass_phrase=SECRET_PHRASE)
        reg_response = await register_uc.execute(reg_request)
        assert reg_response.success is True

    game_action_uc = GameActionUseCase(game_state=game_state_cache)

    await game_action_uc.execute(client1_id)
    await game_action_uc.execute(client2_id)
    await game_action_uc.execute(client1_id)

    result1 = await game_action_uc.execute(client1_id)
    result2 = await game_action_uc.execute(client2_id)
    assert result1 == 3
    assert result2 == 2

    await game_action_uc.execute(client2_id)
    await game_action_uc.execute(client2_id)
    await game_action_uc.execute(client2_id)

    result1 = await game_action_uc.execute(client1_id)
    result2 = await game_action_uc.execute(client2_id)
    assert result1 == 4
    assert result2 == 6


    game1 = await game_state_cache.get_game(client1_id)
    game2 = await game_state_cache.get_game(client2_id)
    assert len(game1.taps) == 4
    assert len(game2.taps) == 6
