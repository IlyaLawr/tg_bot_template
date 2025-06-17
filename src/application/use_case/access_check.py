from domain.interfaces.unit_of_work import IUnitOfWork

from domain.entities.user import User
from application.dto import CheckUserResponse


class AccessCheckUseCase:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow


    async def execute(self, client_id: int) -> CheckUserResponse:
        async with self._uow as uow:
            user: User | None = await uow.user_repository.get(client_id)
            if user is not None and user.access:
                return CheckUserResponse(success=True, message='Вы уже зарегистрированы!')

            return CheckUserResponse(success=False, message='Введите секретную фразу:')
