from typing import Optional
from fastapi import FastAPI

import aioredis

from blog_manager import Blog, BlogManager

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    redis_pool = aioredis.ConnectionPool.from_url('redis://localhost', max_connections=5)
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
async def delete_blog(blog_id: int):
    await app.state.blog_manager.remove_blog_by_id(blog_id)

@app.get('/blogs/{blog_id}')
async def get_blog_by_id(blog_id: int) -> Optional[Blog]:
    return await app.state.blog_manager.get_blog_by_id(blog_id)
