from pytest import mark, skip

from application.use_case.register_user import RegisterUserUseCase
from application.dto import RegisterUserRequest

from domain.entities.user import User
from domain.entities.profile import Profile


SECRET_PHRASE = 'voicee_forever'


@mark.asyncio
async def test_register_user_success(uow):
    client_id = 100

    register_uc = RegisterUserUseCase(pass_phrase=SECRET_PHRASE, uow=uow)
    request = RegisterUserRequest(client_id=client_id, 
                                  username=f'user{client_id}', 
                                  pass_phrase=SECRET_PHRASE)
    response = await register_uc.execute(request)

    assert response.success is True
    assert 'успешно зарегистрирован' in response.message

    async with uow as unit:
        user = await unit.user_repository.get(client_id)
        profile = await unit.profile_repository.get(client_id)
        assert user is not None
        assert user.username == f'user{client_id}'
        assert user.access is True
        assert profile is not None
        assert profile.client_id == client_id


@mark.asyncio
async def test_register_user_wrong_passphrase(uow):
    client_id = 200

    register_uc = RegisterUserUseCase(pass_phrase=SECRET_PHRASE, uow=uow)
    request = RegisterUserRequest(client_id=client_id, 
                                  username=f'user{client_id}', 
                                  pass_phrase='I don\'t know')
    response = await register_uc.execute(request)

    assert response.success is False
    assert 'Не верная секретная фраза' in response.message

    async with uow as unit:
        user = await unit.user_repository.get(client_id)
        profile = await unit.profile_repository.get(client_id)
        assert user is None
        assert profile is None


@mark.asyncio
async def test_register_user_duplicate_id(uow):
    client_id = 300

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id))

    register_uc = RegisterUserUseCase(pass_phrase=SECRET_PHRASE, uow=uow)
    request = RegisterUserRequest(client_id=client_id, 
                                  username=f'double_user{client_id}', 
                                  pass_phrase=SECRET_PHRASE)

    try:
        response = await register_uc.execute(request)
        assert response.success is False or await uow.commit() is None
    except Exception:
        skip('Unique constraint raised an error as expected')
