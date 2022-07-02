from typing import Optional, List
from datetime import datetime, timezone

import asyncpg
from pydantic import BaseModel

from database_query import DBMixin


class Blog(BaseModel):
    id: Optional[int] = None
    title: str
    body: str
    created: str
    published: bool
    user_id: int    
       

class BlogManager(DBMixin):
    def __init__(self, pg: asyncpg.Pool):
        super().__init__(pg)
        self.storage: asyncpg.Pool = pg

    async def add_blog(self, blog: Blog):
        async with self.storage.acquire() as conn:
            dt = datetime.now(timezone.utc)
            return await self.execute('INSERT INTO blogs (title, body, created, published) VALUES ($1, $2, $3, $4)',
                blog.title, blog.body, dt, blog.published
                )                            
               
    async def get_blog_by_id(self, blog_id: int) -> Optional[Blog]:
        return await self.fetch('SELECT * FROM blogs WHERE ID=($1)', blog_id)                 
    
    async def remove_blog_by_id(self, blog_id: int):
        return await self.execute('DELETE FROM blogs WHERE ID=($1)', blog_id)       
               
    async def get_blogs(self) -> List[Blog]:
        return await self.fetch(query='SELECT * FROM blogs')
