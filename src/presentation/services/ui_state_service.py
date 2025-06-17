from abc import ABC, abstractmethod

import redis.asyncio as redis


class UIStateServiceInterface(ABC):
    @abstractmethod
    async def set(self, id: int, state: str) -> None:
        pass 


    @abstractmethod
    async def get(self, id: int) -> str:
        pass
    

    @abstractmethod
    async def clear(self, id: int) -> None:
        pass


class RedisUIStateService(UIStateServiceInterface):
    def __init__(self, redis_client: redis.Redis) -> None:
        self._redis = redis_client
        self._key = f'state:'


    async def set(self, id: int, state: str) -> None:
        await self._redis.set(f'{self._key}{id}', state)


    async def get(self, id: int) -> str | None:
        raw =  await self._redis.get(f'{self._key}{id}')
        if raw is None:
            return None

        return raw.decode('utf-8')


    async def clear(self, id: int) -> None:
        await self._redis.delete(f'{self._key}{id}')
