from pytest import mark

from application.use_case.filling_profile import FillingProfileUseCase
from application.dto import FormUserRequest
from application.use_case.update_profile import UpdateProfileUseCase

from domain.entities.user import User
from domain.entities.profile import Profile


@mark.asyncio
async def test_filling_profile_flow(uow, profile_state_cache, photo_storage, answer_validator):
    client_id = 100

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id))

    update_uc = UpdateProfileUseCase(profile_state_cache, photo_storage, uow)
    fill_uc = FillingProfileUseCase(state_cache=profile_state_cache,
                                    profile_update_use_case=update_uc,
                                    validator=answer_validator)
 
    request1 = FormUserRequest(client_id=client_id, content='')
    response1 = await fill_uc.execute(request1)

    assert response1.success is True
    assert response1.message == answer_validator.questions[1]

    request2 = FormUserRequest(client_id=client_id, content='Дональд Трамп')
    response2 = await fill_uc.execute(request2)

    assert response2.success is True
    assert response2.message == answer_validator.questions[2]

    question_number = await profile_state_cache.get_question_number(client_id)
    assert question_number == 2

    about_text = 'Хочу вступить в войну с Ираном.'
    request3 = FormUserRequest(client_id=client_id, content=about_text)
    response3 = await fill_uc.execute(request3)

    assert response3.success is True
    assert response3.message == answer_validator.questions[3]

    fake_photo = b'\xff\xd8\xff'
    request4 = FormUserRequest(client_id=client_id, content=fake_photo)
    response4 = await fill_uc.execute(request4)

    assert response4.success is True
    assert response4.complete is True
    assert 'успешно заполнена' in response4.message

    async with uow as unit:
        profile = await unit.profile_repository.get(client_id)
        assert profile.name == 'Дональд Трамп'
        assert profile.about == about_text
        assert profile.photo != ''

    updates = await profile_state_cache.get_profile_updates(client_id)
    assert updates == {}


@mark.asyncio
async def test_filling_profile_invalid_answer(answer_validator, uow, profile_state_cache):
    client_id = 200

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id))

    update_uc = UpdateProfileUseCase(profile_state_cache, None, uow)
    fill_uc = FillingProfileUseCase(state_cache=profile_state_cache,
                                    profile_update_use_case=update_uc,
                                    validator=answer_validator)

    await profile_state_cache.set_question_number(client_id, 1)

    request = FormUserRequest(client_id=client_id, content='777')
    response = await fill_uc.execute(request)

    assert response.success is False
    assert response.error is not None
    assert response.message == ''
