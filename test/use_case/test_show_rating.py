from pytest import mark

from application.use_case.show_rating import ShowRatingUseCase
from domain.entities.user import User
from domain.entities.profile import Profile

@mark.asyncio
async def test_show_rating_basic(uow):
    client1_id, client2_id, client3_id = 100, 200, 300

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client1_id, 
                                               username=f'user{client1_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client1_id, 
                                                     name='Игорек', 
                                                     about='', 
                                                     photo='', 
                                                     taps_statistics=5))
    
        await unit.user_repository.create(User(client_id=client2_id, 
                                               username=f'user{client2_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client2_id, 
                                                     name='Эдуард Суровый', 
                                                     about='', 
                                                     photo='', 
                                                     taps_statistics=7))
    
        await unit.user_repository.create(User(client_id=client3_id, 
                                               username=f'user{client3_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client3_id, 
                                                     name='Жорик Вартанов', 
                                                     about='', 
                                                     photo='', 
                                                     taps_statistics=3))

    rating_uc = ShowRatingUseCase(uow)
    response = await rating_uc.execute(client1_id)

    assert response is not None
    assert response.all_count_tap == 15
    assert response.user_count_tap == 5
    assert response.leader_username == f'user{client2_id}'
    assert response.leader_name == 'Эдуард Суровый'
    assert response.leader_count_tap == 7


@mark.asyncio
async def test_show_rating_single_user(uow):
    client_id = 400

    async with uow as unit:
        await unit.user_repository.create(User(client_id=client_id, 
                                               username=f'user{client_id}', 
                                               access=True))
        await unit.profile_repository.create(Profile(client_id=client_id, 
                                                     name='Маркелов', 
                                                     about='', 
                                                     photo='', 
                                                     taps_statistics=2))

    rating_uc = ShowRatingUseCase(uow)
    response = await rating_uc.execute(client_id)

    assert response.all_count_tap == 2
    assert response.user_count_tap == 2
    assert response.leader_count_tap == 2
    assert response.leader_username == f'user{client_id}'
    assert response.leader_name == 'Маркелов'


@mark.asyncio
async def test_show_rating_user_not_exists(uow):
    client_id = 500

    rating_uc = ShowRatingUseCase(uow)
    response = await rating_uc.execute(client_id)
    assert response is None
