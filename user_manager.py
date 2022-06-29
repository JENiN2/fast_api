from typing import Optional, List

from fastapi import HTTPException, status
import asyncpg
from pydantic import BaseModel

from hashing import Hash

class User(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    password: str


class UserLogin(BaseModel):
    first_name: str
    password: str    


class UserManager:
    def __init__(self, pg: asyncpg.Pool):
        self.storage: asyncpg.Pool = pg      

    async def add_user(self, user: User):
        async with self.storage.acquire() as conn:            
            await conn.execute('''
               INSERT INTO users (first_name, last_name, password) VALUES ($1, $2, $3)
            ''', user.first_name, user.last_name, Hash.bcrypt(user.password))

    async def get_users(self) -> List[User]:
        async with self.storage.acquire() as conn:
            return await conn.fetch('''
               SELECT * FROM users
            ''')

    async def login_user(self, login: UserLogin):
        async with self.storage.acquire() as conn:
            user = await conn.fetchrow('''
               SELECT first_name, password FROM users WHERE first_name=($1)
            ''', login.first_name) 
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')                                                
            if not Hash.verify(user['password'], login.password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect Password')            
            return user     

    async def remove_user_by_id(self, user_id: int):
        async with self.storage.acquire() as conn:
            await conn.execute('''
               DELETE FROM users WHERE ID=($1)
            ''', user_id)  
