from functools import lru_cache
from typing import Optional

from fastapi import FastAPI, Depends
import uvicorn
import asyncpg

from blog_manager import Blog, BlogManager
from config import Config

app = FastAPI()
cfg = Config()


@lru_cache(maxsize=None)
def get_blog_manager() -> BlogManager:    
    return BlogManager(app.state.pg_pool)


@app.on_event('startup')
async def startup():
    app.state.pg_pool = await asyncpg.create_pool(
        f'postgres://{cfg.pg_user}:{cfg.pg_password}@{cfg.pg_host}:{cfg.pg_port}/{cfg.pg_db}',
        min_size=cfg.pg_pool_min_size,
        max_size=cfg.pg_pool_max_size
    )  


@app.get('/blogs')
async def get_blogs(bm: BlogManager = Depends(get_blog_manager)):
    return await bm.get_blogs()


@app.post('/blogs')
async def create_blog(blog: Blog, bm: BlogManager = Depends(get_blog_manager)):
    await bm.add_blog(blog)


@app.delete('/blogs/{blog_id}')
async def delete_blog(blog_id: int, bm: BlogManager = Depends(get_blog_manager)):
    await bm.remove_blog_by_id(blog_id)


@app.get('/blogs/{blog_id}')
async def get_blog_by_id(blog_id: int, bm: BlogManager = Depends(get_blog_manager)) -> Optional[Blog]:
    return await bm.get_blog_by_id(blog_id)


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=cfg.app_server_host,
        port=cfg.app_server_port
    )
