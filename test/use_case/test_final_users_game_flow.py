from pytest import mark

from application.use_case.access_check import AccessCheckUseCase
from application.use_case.register_user import RegisterUserUseCase
from application.use_case.filling_profile import FillingProfileUseCase
from application.use_case.update_profile import UpdateProfileUseCase
from application.use_case.game_action import GameActionUseCase
from application.use_case.saving_game_results import SavingGameResultUseCase
from application.use_case.show_rating import ShowRatingUseCase
from application.dto import RegisterUserRequest, FormUserRequest


SECRET_PHRASE = 'voicee_forever'


@mark.asyncio
async def test_three_users_game_flow(uow, game_state_cache,
                                     profile_state_cache, photo_storage,
                                     answer_validator):

    client1_id = 100
    access_uc = AccessCheckUseCase(uow=uow)
    response = await access_uc.execute(client1_id)
    assert response.success is False

    register_uc = RegisterUserUseCase(pass_phrase=SECRET_PHRASE, uow=uow)
    reg_request = RegisterUserRequest(client_id=client1_id,
                                      username=f'user{client1_id}',
                                      pass_phrase=SECRET_PHRASE)
    reg_response = await register_uc.execute(reg_request)
    assert reg_response.success is True

    game_uc = GameActionUseCase(game_state=game_state_cache)
    taps1_a = await game_uc.execute(client1_id)
    taps1_b = await game_uc.execute(client1_id)
    assert taps1_a == 1
    assert taps1_b == 2

    save_uc = SavingGameResultUseCase(game_state=game_state_cache, uow=uow)
    await save_uc.execute(client1_id)
    async with uow as unit:
        profile1 = await unit.profile_repository.get(client1_id)
        assert profile1.taps_statistics == 2


    client2_id = 200
    reg_request = RegisterUserRequest(client_id=client2_id,
                                      username=f'user{client2_id}',
                                      pass_phrase=SECRET_PHRASE)
    reg_response = await register_uc.execute(reg_request)
    assert reg_response.success is True

    update_uc = UpdateProfileUseCase(state_cache=profile_state_cache,
                                     photo_storage_service=photo_storage,
                                     uow=uow)
    fill_uc = FillingProfileUseCase(state_cache=profile_state_cache,
                                    profile_update_use_case=update_uc,
                                    validator=answer_validator)

    fake_photo = b'\xff\xd8\xff'
    resp = await fill_uc.execute(FormUserRequest(client_id=client2_id, content=''))
    resp = await fill_uc.execute(FormUserRequest(client_id=client2_id, content='Павел'))
    resp = await fill_uc.execute(FormUserRequest(client_id=client2_id, content='Лучший игрок в данном тесте'))
    resp = await fill_uc.execute(FormUserRequest(client_id=client2_id, content=fake_photo))
    assert resp.complete is True

    async with uow as unit:
        profile2 = await unit.profile_repository.get(client2_id)
        assert profile2.name == 'Павел'
        assert profile2.about == 'Лучший игрок в данном тесте'
        assert profile2.photo != ''

    taps2_a = await game_uc.execute(client2_id)
    taps2_b = await game_uc.execute(client2_id)
    taps2_c = await game_uc.execute(client2_id)
    assert taps2_a == 1 and taps2_b == 2 and taps2_c == 3

    await save_uc.execute(client2_id)
    async with uow as unit:
        profile2 = await unit.profile_repository.get(client2_id)
        assert profile2.taps_statistics == 3


    client3_id = 300
    reg_request = RegisterUserRequest(client_id=client3_id,
                                      username=f'user{client3_id}',
                                      pass_phrase=SECRET_PHRASE)
    reg_response = await register_uc.execute(reg_request)
    assert reg_response.success is True

    taps3 = await game_uc.execute(client3_id)
    assert taps3 == 1

    await save_uc.execute(client3_id)
    async with uow as unit:
        profile3 = await unit.profile_repository.get(client3_id)
        assert profile3.taps_statistics == 1


    rating_uc = ShowRatingUseCase(uow=uow)
    rating_response = await rating_uc.execute(client1_id)

    total_taps = 2 + 3 + 1
    assert rating_response.all_count_tap == total_taps
    assert rating_response.user_count_tap == 2
    assert rating_response.leader_count_tap == 3
    assert rating_response.leader_username == f'user{client2_id}'
    assert rating_response.leader_name == 'Павел'
