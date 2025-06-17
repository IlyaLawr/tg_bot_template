from domain.interfaces.unit_of_work import IUnitOfWork

from domain.entities.user import User
from domain.entities.profile import Profile

from application.dto import RegisterUserRequest, RegisterUserResponse


class RegisterUserUseCase:
    def __init__(self, pass_phrase: str, uow: IUnitOfWork):
        self._uow = uow
        self._pass_phrase = pass_phrase


    async def execute(self, request: RegisterUserRequest) -> RegisterUserResponse:
        if not request.pass_phrase == self._pass_phrase:
            return RegisterUserResponse(success=False,
                                        message='Не верная секретная фраза.')

        user: User = User(client_id=request.client_id,
                          username=request.username,
                          access=True)

        profile: Profile = Profile(client_id=request.client_id)

        async with self._uow as uow:
            await uow.user_repository.create(user)
            await uow.profile_repository.create(profile)

        return RegisterUserResponse(success=True,
                                    message='Пользователь успешно зарегистрирован. Обязательно заполните профиль.')
