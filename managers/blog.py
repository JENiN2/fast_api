from typing import Optional, List
from datetime import datetime, timezone

from fastapi import HTTPException, status

from .base import BaseManager
from schemas import Blog


class BlogManager(BaseManager):
    async def add_blog(self, blog: Blog, user_id: int):
        async with self.pg.acquire() as conn:
            blog.created = datetime.now(timezone.utc)
            await self.execute('INSERT INTO blogs (title, body, created, published, user_id) VALUES ($1, $2, $3, $4, $5)',
                blog.title, blog.body, blog.created, blog.published, user_id
                )
            return blog                            
               
    async def get_blog_by_id(self, blog_id: int) -> Optional[Blog]:
        blog = await self.fetch('SELECT * FROM blogs WHERE ID=($1)', blog_id)
        if blog == []:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Blog with id {blog_id} does not exist',
                    )           
        else:
            return blog

    async def remove_blog_by_id(self, blog_id: int):
        if await self.execute('DELETE FROM blogs WHERE ID=($1)', blog_id) == 'DELETE 0':
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Blog with id {blog_id} does not exist',
                    )
        else:
            return {'detail': f'Blog with id {blog_id} is deleted'} 

    async def get_blogs(self) -> List[Blog]:
        return await self.fetch(query='SELECT * FROM blogs')
