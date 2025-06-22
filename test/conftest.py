from os import getenv
from pathlib import Path

import redis.asyncio as redis
from pytest_asyncio import fixture as asyncio_fixture
from pytest import fixture
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from infrastructure.sql_alchemy_uow import SqlAlchemyUnitOfWork
from infrastructure.repositories.sql_user_repository import SQLUserRepository
from infrastructure.repositories.sql_profile_repository import SQLProfileRepository
from infrastructure.database.models import Base
from infrastructure.state_cache.redis_game_state_cache import RedisGameStateCache
from infrastructure.state_cache.redis_profile_filling_state_cache import RedisProfileFillingStateCache
from infrastructure.disk_photo_stogare_service import DiskPhotoStorageService

from domain.factories.game_factory import GameFactory
from domain.services.answer_validation import AnswerValidationService


db_user = getenv('DB_USER', 'postgres')
db_password = getenv('DB_PASSWORD')
db_host = getenv('DB_HOST', 'localhost')
db_port = getenv('DB_PORT', '5432')
db_name = getenv('DB_NAME', 'postgres_test')

redis_host = getenv('REDIS_HOST', 'localhost')
redis_port = getenv('REDIS_PORT', '6379')
redis_db_num = getenv('REDIS_DB_NUM', '1')


if db_password:
    DB_URL = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
else:
    DB_URL = f'postgresql+asyncpg://{db_user}@{db_host}:{db_port}/{db_name}'

REDIS_URL = f'redis://{redis_host}:{redis_port}/{redis_db_num}'

TMP_PATH = Path('../tmp_photo_storage/')


@asyncio_fixture(scope='session', autouse=True)
async def create_test_database():
    admin_db_url = DB_URL.replace('/postgres_test', '/postgres')
    engine = create_async_engine(admin_db_url)
    async with engine.connect() as conn:
        try:
            await conn.execute(text('CREATE DATABASE postgres_test'))
        except Exception:
            pass 
    yield


@asyncio_fixture(scope='session')
async def db_engine():
    engine = create_async_engine(DB_URL, future=True, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@asyncio_fixture(autouse=True)
async def prepare_db(db_engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@asyncio_fixture
async def uow():
    uow = SqlAlchemyUnitOfWork(DB_URL, SQLUserRepository, SQLProfileRepository)
    yield uow
    await uow._engine.dispose()


@asyncio_fixture(scope='session')
async def redis_client():
    client = redis.from_url(url=REDIS_URL, encoding='utf-8', decode_responses=False)
    yield client
    await client.aclose()


@asyncio_fixture(autouse=True, scope='module')
async def clean_redis(redis_client):
    await redis_client.flushdb()
    yield


@fixture(scope='session', autouse=True)
def clean_tmp_storage():
    def _clean():
        for item in TMP_PATH.iterdir():
            if item.is_file() and item.name.endswith('.jpg'):
                item.unlink()
    _clean()
    yield
    _clean()


@asyncio_fixture
def game_state_cache(redis_client):
    return RedisGameStateCache(redis_client=redis_client, game_factory=GameFactory())


@asyncio_fixture
def profile_state_cache(redis_client):
    return RedisProfileFillingStateCache(redis_client=redis_client)


@fixture
def photo_storage():
    return DiskPhotoStorageService(base_path=TMP_PATH)


@fixture
def answer_validator():
    return AnswerValidationService()
