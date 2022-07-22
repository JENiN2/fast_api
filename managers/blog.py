from typing import Optional, List
from datetime import datetime, timezone

from .base import BaseManager
from schemas import Blog


class BlogManager(BaseManager):
    async def add_blog(self, blog: Blog, user_id: int):
        async with self.pg.acquire() as conn:
            dt = datetime.now(timezone.utc)
            return await self.execute('INSERT INTO blogs (title, body, created, published, user_id) VALUES ($1, $2, $3, $4, $5)',
                blog.title, blog.body, dt, blog.published, user_id
                )                            
               
    async def get_blog_by_id(self, blog_id: int) -> Optional[Blog]:
        return await self.fetch('SELECT * FROM blogs WHERE ID=($1)', blog_id)                 
    
    async def remove_blog_by_id(self, blog_id: int):
        return await self.execute('DELETE FROM blogs WHERE ID=($1)', blog_id)       
               
    async def get_blogs(self) -> List[Blog]:
        return await self.fetch(query='SELECT * FROM blogs')
