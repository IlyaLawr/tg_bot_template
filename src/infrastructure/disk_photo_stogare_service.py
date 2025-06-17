from aiofiles import open
from pathlib import Path

from domain.interfaces.photo_storage_service import IPhotoStorageService


class DiskPhotoStorageService(IPhotoStorageService):
    def __init__(self, base_path: Path) -> None:
        self._base_path = base_path


    async def save(self, user_id: int, file_bytes: bytes) -> str:
        file_path = self._base_path / f'{user_id}.jpg'

        async with open(file_path, 'wb') as file:
            await file.write(file_bytes)

        return str(file_path)
