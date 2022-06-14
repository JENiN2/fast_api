from typing import Optional

from fastapi import FastAPI
import aioredis
from pydantic import UUID4

from blog_manager import Blog, BlogManager
from config import Config

app = FastAPI()
cfg = Config()
app.state.config = cfg

@app.on_event("startup")
async def startup_event():
    redis_host = app.state.config.redis_host
    redis_pool_max_conn = app.state.config.redis_pool_max_conn
    redis_pool = aioredis.ConnectionPool.from_url(
        'redis://{}'.format(redis_host),
        max_connections=redis_pool_max_conn,
    )
    redis = aioredis.Redis(connection_pool=redis_pool)
    app.state.blog_manager = BlogManager(redis)

@app.on_event('shutdown')
async def shutdown_event():
    pass

@app.get('/blogs')
async def get_blogs():
    return await app.state.blog_manager.get_blogs()

@app.post('/blogs')
async def create_blog(blog: Blog):
    await app.state.blog_manager.add_blog(blog)

@app.delete('/blogs/{blog_id}')
async def delete_blog(blog_id: UUID4):
    await app.state.blog_manager.remove_blog_by_id(blog_id)

@app.get('/blogs/{blog_id}')
async def get_blog_by_id(blog_id: UUID4) -> Optional[Blog]:
    return await app.state.blog_manager.get_blog_by_id(blog_id)


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=cfg.app_server_host,
        port=cfg.app_server_port
    )
