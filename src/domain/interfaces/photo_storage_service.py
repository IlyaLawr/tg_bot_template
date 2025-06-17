from abc import ABC, abstractmethod


class IPhotoStorageService(ABC):
    @abstractmethod
    async def save(self, id: int, file_bytes: bytes) -> str:
        pass
