import redis.asyncio as redis

from domain.interfaces.state_cache.game_state_cache import IGameStateCache
from domain.factories.game_factory import IGameFactory
from domain.entities.game import Game
from domain.entities.tap import Tap


class RedisGameStateCache(IGameStateCache):
    def __init__(self, 
                 redis_client: redis.Redis,
                 game_factory: IGameFactory) -> None:

        self._redis = redis_client
        self._game_factory = game_factory


    def _get_stream_key(self, game_id: int) -> str:
        return f'game_stream:{game_id}'


    async def add_tap(self, game_id: int, tap: Tap) -> None:
        stream_key = self._get_stream_key(game_id)
        
        tap_data = {'id': str(tap.id),
                    'timestamp': tap.timestamp.isoformat()}
        
        await self._redis.xadd(stream_key, tap_data)


    async def get_game(self, game_id: int) -> Game:
        stream_key = self._get_stream_key(game_id)
        taps_data: list[dict[str, str]] = []

        last_id = '0-0'
        chunk_size = 100

        while True:
            response = await self._redis.xread(streams={stream_key: last_id},
                                               count=chunk_size)
            if not response:
                break

            messages = response[0][1]
            for _, data_dict in messages:
                decoded: dict[str, str] = {}
                for key_b, val_b in data_dict.items():
                    key = key_b.decode('utf-8')
                    val = val_b.decode('utf-8')
                    decoded[key] = val
                taps_data.append(decoded)


            last_id = messages[-1][0]

        return self._game_factory.create_game(game_id=game_id,
                                              taps_data=taps_data)


    async def clear_game(self, game_id: int) -> None:
        stream_key = self._get_stream_key(game_id)
        await self._redis.delete(stream_key)
