from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = Field(env='REDIS_HOST', default='localhost')
    redis_port: int = Field(env='REDIS_PORT', default=6379)

    db_host: str = Field(env='DB_HOST', default='localhost')
    db_port: int = Field(env='DB_PORT', default=5432)
    db_user: str = Field(env='DB_USER', default='postgres')
    db_password: str = Field(env='DB_PASSWORD', default=None)
    db_name: str = Field(env='DB_NAME', default='postgres')

    db_logs: bool = True

    bot_token: str = Field(env='BOT_TOKEN')
    pass_phrase: str = Field(env='PASS_PHRASE')

    base_path: Path = Path(__file__).resolve().parent


    @property
    def db_url(self) -> str:
        password = f':{self.db_password}' if self.db_password else ''
        return f'postgresql+asyncpg://{self.db_user}{password}@{self.db_host}:{self.db_port}/{self.db_name}'


    @property
    def redis_url(self) -> str:
        return f'redis://{self.redis_host}:{self.redis_port}'


    @property
    def photo_storage(self) -> str:
        return self.base_path / 'photo_storage'


    class Config:
        env_file = str('.//.env')
        env_file_encoding = 'utf-8'


settings = Settings()
