from typing import Optional, List
from datetime import datetime, timezone

import asyncpg
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    password: str


class UserManager:
    def __init__(self, pg: asyncpg.Pool):
        self.storage: asyncpg.Pool = pg      

    async def add_user(self, user: User):
        async with self.storage.acquire() as conn:            
            await conn.execute('''
               INSERT INTO users (first_name, last_name, password) VALUES ($1, $2, $3)
            ''', user.first_name, user.last_name, user.password)

    async def get_users(self) -> List[User]:
        async with self.storage.acquire() as conn:
            return await conn.fetch('''
               SELECT * FROM users
            ''')

    async def remove_user_by_id(self, user_id: int):
        async with self.storage.acquire() as conn:
            await conn.execute('''
               DELETE FROM users WHERE ID=($1)
            ''', user_id)  
