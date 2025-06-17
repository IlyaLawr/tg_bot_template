from abc import ABC, abstractmethod


class IProfileFillingStateCache(ABC):
    @abstractmethod
    async def get_question_number(self, client_id: int) -> int | None:
        pass


    @abstractmethod
    async def set_question_number(self, client_id: int, index: int) -> None:
        pass


    @abstractmethod
    async def set_field_answer(client_id: int, field_name: str, answer: str) -> None:
        pass


    @abstractmethod
    async def get_profile_updates(client_id: int) -> dict[str, str]:
        pass

    @abstractmethod
    async def clear_current_index(client_id: int) -> None:
        pass


    @abstractmethod
    async def clear(self, user_id: int) -> None:
        pass
