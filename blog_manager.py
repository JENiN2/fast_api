from typing import Optional, List

import asyncpg
from pydantic import BaseModel


class Blog(BaseModel):
    id: Optional[int] = None
    title: str
    body: str
    published: bool
                

class BlogManager:
    def __init__(self, pg: asyncpg.Pool):
        self.storage: asyncpg.Pool = pg

    async def add_blog(self, blog: Blog):
        async with self.storage.acquire() as conn:
            await conn.execute('''
               INSERT INTO blogs (title, body, published) VALUES ($1, $2, $3)
            ''', blog.title, blog.body, blog.published)                      
                
    async def get_blog_by_id(self, blog_id: int) -> Optional[Blog]:
        async with self.storage.acquire() as conn:
            return await conn.fetch('''
               SELECT * FROM blogs WHERE ID=($1)
            ''', blog_id)        
    
    async def remove_blog_by_id(self, blog_id: int):
        async with self.storage.acquire() as conn:
            await conn.execute('''
               DELETE FROM blogs WHERE ID=($1)
            ''', blog_id)    

    async def get_blogs(self) -> List[Blog]:
        async with self.storage.acquire() as conn:
            return await conn.fetch('''
               SELECT * FROM blogs
            ''')
