import redis.asyncio as redis

from domain.interfaces.state_cache.profile_filling_state_cache import IProfileFillingStateCache


class RedisProfileFillingStateCache(IProfileFillingStateCache):
    def __init__(self, redis_client: redis.Redis) -> None:
        self._redis = redis_client


    async def get_question_number(self, client_id: int) -> int | None:
        raw = await self._redis.get(f'{client_id}:q_idx')
        if raw is None:
            return None
 
        return int(raw.decode('utf-8'))


    async def set_question_number(self, client_id: int, index: int) -> None:
        await self._redis.set(f'{client_id}:q_idx', str(index))


    async def set_field_answer(self, client_id: int, field_name: str, answer: str | bytes) -> None:
        await self._redis.hset(f'{client_id}:p_upd', field_name, answer)


    async def get_profile_updates(self, client_id: int) -> dict[str, str]:
        raw_dict = await self._redis.hgetall(f'{client_id}:p_upd')
        if not raw_dict:
            return {}
  
        decoded: dict[str, str] = {}
        for key_b, val_b in raw_dict.items():
            try:
                key = key_b.decode('utf-8')
                val = val_b.decode('utf-8')
                decoded[key] = val
            except UnicodeDecodeError:
                decoded[key_b.decode('utf-8')] = val_b

        return decoded


    async def clear_current_index(self, client_id: int) -> None:
        await self._redis.delete(f'{client_id}:q_idx')


    async def clear(self, client_id: int) -> None:
        await self._redis.delete(f'{client_id}:q_idx', f'{client_id}:p_upd')
