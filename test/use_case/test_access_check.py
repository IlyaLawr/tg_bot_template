from pytest import mark

from application.use_case.access_check import AccessCheckUseCase
from application.dto import CheckUserResponse

from domain.entities.user import User
from domain.entities.profile import Profile


@mark.asyncio
async def test_access_check_no_user(uow):
    client_id = 100

    access_uc = AccessCheckUseCase(uow=uow)
    response: CheckUserResponse = await access_uc.execute(client_id)

    assert response.success is False
    assert 'секретную фразу' in response.message


@mark.asyncio
async def test_access_check_user_without_access(uow):
    client_id = 200

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=False))
        await unit.profile_repository.create(Profile(client_id=client_id))

    access_uc = AccessCheckUseCase(uow=uow)
    response: CheckUserResponse = await access_uc.execute(client_id)

    assert response.success is False
    assert 'секретную фразу' in response.message


@mark.asyncio
async def test_access_check_user_with_access(uow):
    client_id = 300

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id))

    access_uc = AccessCheckUseCase(uow=uow)
    response: CheckUserResponse = await access_uc.execute(client_id)

    assert response.success is True
    assert 'зарегистрированы' in response.message
