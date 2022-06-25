from functools import lru_cache
from multiprocessing import Pool
from typing import Optional
import asyncio

from fastapi import FastAPI, Depends
from pydantic import UUID4
import uvicorn
import aioredis
import asyncpg

from blog_manager import Blog, BlogManager
from config import Config

app = FastAPI()
cfg = Config()
app.state.config = cfg


@lru_cache(maxsize=None)
def get_redis_pool() -> aioredis.Redis:
    return aioredis.Redis(connection_pool = aioredis.ConnectionPool.from_url(
        'redis://{}'.format('localhost'),
        max_connections=5,
    ))


@lru_cache(maxsize=None)
def get_blog_manager() -> BlogManager:  
    return BlogManager(get_redis_pool())


@app.get('/blogs')
async def get_blogs(bm: BlogManager = Depends(get_blog_manager)):
    print(bm)  
    return await bm.get_blogs()


@app.post('/blogs')
async def create_blog(blog: Blog, bm: BlogManager = Depends(get_blog_manager)):
    await bm.add_blog(blog)


@app.delete('/blogs/{blog_id}')
async def delete_blog(blog_id: UUID4, bm: BlogManager = Depends(get_blog_manager)):
    await bm.remove_blog_by_id(blog_id)


@app.get('/blogs/{blog_id}')
async def get_blog_by_id(blog_id: UUID4, bm: BlogManager = Depends(get_blog_manager)) -> Optional[Blog]:
    return await bm.get_blog_by_id(blog_id)


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=cfg.app_server_host,
        port=cfg.app_server_port
    )
