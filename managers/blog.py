from typing import Optional, List
from datetime import datetime, timezone

from .base import BaseManager
from schemas import Blog
import schemas


class BlogManager(BaseManager):
    async def add_blog(self, blog: Blog):
        async with self.pg.acquire() as conn:
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
