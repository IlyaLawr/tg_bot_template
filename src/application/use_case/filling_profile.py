from domain.interfaces.state_cache.profile_filling_state_cache import IProfileFillingStateCache

from application.dto import FormUserRequest, FormUserResponse
from application.use_case.update_profile import UpdateProfileUseCase
from domain.services.answer_validation import AnswerValidationService


class FillingProfileUseCase:

    _FIELD_MAP = {1: 'name', 2: 'about', 3: 'photo'}

    def __init__(self,
                 state_cache: IProfileFillingStateCache,
                 profile_update_use_case: UpdateProfileUseCase,
                 validator: AnswerValidationService) -> None:

        self._state_cache = state_cache
        self._profile_update_use_case = profile_update_use_case
        self._validator_answer = validator
        self._questions = validator.questions


    async def execute(self, request: FormUserRequest) -> FormUserResponse:
        if not request.content:
            await self._state_cache.set_question_number(request.client_id, 1)
            first_question = self._questions.get(1)
            return FormUserResponse(True, first_question)

        question_number = await self._state_cache.get_question_number(request.client_id)

        result = self._validator_answer.check(request.content, question_number)
        if not result.valid:
            return FormUserResponse(False, message='', error=result.error)

        if field := self._FIELD_MAP.get(question_number):
            await self._state_cache.set_field_answer(request.client_id, field, request.content)

        next_question_number = question_number + 1
        if next_question := self._questions.get(next_question_number):
            await self._state_cache.set_question_number(request.client_id, next_question_number)
            return FormUserResponse(True, next_question)
        else:
            await self._profile_update_use_case.execute(request.client_id)
            return FormUserResponse(True, 'Анкета успешно заполнена!', complete=True)
