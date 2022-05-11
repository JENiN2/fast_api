from pydantic import BaseSettings, Field


class Config(BaseSettings):
    redis_host: str = Field(default='localhost', env='REDIS_HOST')
    redis_pool_max_conn: int = Field(default=5, env='REDIS_POOL_MAX_CONN')
    app_server_port: int = Field(default=8000, env='SERVER_PORT')
    app_server_host: str = Field(default='127.0.0.1', env='SERVER_HOST')
