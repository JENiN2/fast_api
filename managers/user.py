from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import asyncpg

from jwt_token import create_access_token
from hashing import Hash
from .base import BaseManager
from schemas import User


class UserManager(BaseManager):
    async def add_user(self, user: User):
        print(user, type(user))        
        try:
            return await self.execute('INSERT INTO users (login, first_name, last_name, password) VALUES ($1, $2, $3, $4)',
                user.login, user.first_name, user.last_name, Hash.bcrypt(user.password)
                )
        except asyncpg.exceptions.UniqueViolationError:    
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='login already exists')                 
                
    async def get_users(self) -> List[User]:        
        return await self.fetch(query='SELECT * FROM users')
        
    async def login_user(self, login: OAuth2PasswordRequestForm = Depends()):                 
        user = await self.fetchrow('SELECT first_name, password FROM users WHERE first_name=($1)', login.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Invalid Credentials')                                                
        if not Hash.verify(user['password'], login.password):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Incorrect Password')            
        access_token = create_access_token(data={"sub": login.username})
        return {"access_token": access_token, "token_type": "bearer"}    

    async def remove_user_by_id(self, user_id: int):        
        return await self.execute('DELETE FROM users WHERE ID=($1)', user_id)

    async def get_user_by_name(self, user_name: str):
        #user: User = 
        user = await self.fetchrow('SELECT id FROM users WHERE login=($1)', user_name)       
        return user[0]
