from typing import Optional, List
import json
import uuid

import aioredis
from pydantic import BaseModel, UUID4


class Blog(BaseModel):
    id: Optional[UUID4]
    title: str
    body: str
    published: Optional[bool]

    def set_id(self):
        self.id = str(uuid.uuid4())
                

class BlogManager:
    def __init__(self, redis: aioredis.Redis):
        self.storage: aioredis.Redis = redis

    async def add_blog(self, blog: Blog):
        async with self.storage.client() as conn:
            blog.set_id()
            await conn.set(str(blog.id), blog.json())
    
    async def get_blog_by_id(self, blog_id: int) -> Optional[Blog]:
        async with self.storage.client() as conn:
            data = await conn.get(str(blog_id))
        if not data:
            return None
        parsed_data = json.loads(data.decode())
        return Blog(**parsed_data)
    
    async def remove_blog_by_id(self, id: int):
        await self.storage.execute_command('del', str(id))
    
    async def get_blogs(self) -> List[Blog]:
        async with self.storage.client() as conn:
            keys = map(bytes.decode, await conn.keys('*'))
            data = await conn.mget(keys)
        return [Blog(**json.loads(x)) for x in map(bytes.decode, data)]
