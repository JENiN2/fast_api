from pydantic import BaseSettings, Field


class Config(BaseSettings):
    pg_host: str = Field(default='localhost', env='PG_HOST')
    pg_port: str = Field(default='5432', env='PG_PORT')
    pg_pool_max_size: int = Field(default=20, env='PG_POOL_MAX_SIZE')
    pg_pool_min_size: int = Field(default=10, env='PG_POOL_MIN_SIZE')
    pg_db: str = Field(default='blogs', env='PG_DB') 
    pg_user: str = Field(default='postgres', env='PG_USER')
    pg_password: str = Field(default='123', env='PG_PASSSWORD')
    app_server_port: int = Field(default=8000, env='SERVER_PORT')
    app_server_host: str = Field(default='127.0.0.1', env='SERVER_HOST')
    tk_secret_key: str = Field(default='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7', env='SECRET_KEY')
    tk_algorithm: str = Field(default='HS256', env='ALGORITHM')
    tk_expire_minutes: int = Field(default='30', env='ACCESS_TOKEN_EXPIRE_MINUTES')
  