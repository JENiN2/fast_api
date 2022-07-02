from functools import lru_cache

from starlette.requests import Request

from managers import UserManager, BlogManager
from config import Config

cfg = Config()


@lru_cache(maxsize=None)
def get_blog_manager(request: Request) -> BlogManager:        
    return BlogManager(request.app.state.pg_pool)


@lru_cache(maxsize=None)
def get_user_manager(request: Request) -> UserManager:
    return UserManager(request.app.state.pg_pool)
