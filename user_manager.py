from typing import List

from fastapi import HTTPException, status
import asyncpg

from hashing import Hash
from base_manager import BaseManager
from schemas import User, UserLogin


class UserManager(BaseManager):
    def __init__(self, pg: asyncpg.Pool):
        super().__init__(pg)
        self.storage: asyncpg.Pool = pg         

    async def add_user(self, user: User):        
        try:
            return await self.execute('INSERT INTO users (login, first_name, last_name, password) VALUES ($1, $2, $3, $4)',
                user.login, user.first_name, user.last_name, Hash.bcrypt(user.password)
                )
        except asyncpg.exceptions.UniqueViolationError:    
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='login already exists')
                
    async def get_users(self) -> List[User]:
        return await self.fetch(query='SELECT * FROM users')
        
    async def login_user(self, login: UserLogin):                 
        user = await self.fetchrow('SELECT first_name, password FROM users WHERE first_name=($1)', login.first_name)
        if not user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Invalid Credentials')                                                
        if not Hash.verify(user['password'], login.password):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Incorrect Password')            
        return user     

    async def remove_user_by_id(self, user_id: int):        
        return await self.execute('DELETE FROM users WHERE ID=($1)', user_id)
        