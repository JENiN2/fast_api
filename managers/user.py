from typing import List
from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import asyncpg

from jwt_token import create_access_token
from hashing import Hash
from .base import BaseManager
from schemas import User
from config import Config


cfg = Config()

class UserManager(BaseManager):
    async def add_user(self, user: User):               
        try:
            await self.execute('INSERT INTO users (login, first_name, last_name, password) VALUES ($1, $2, $3, $4)',
                user.login, user.first_name, user.last_name, Hash.bcrypt(user.password)
                )
        except asyncpg.exceptions.UniqueViolationError:    
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='login already exists')
        return {'detai': 'User is registered'}                 
                
    async def get_users(self) -> List[User]:        
        return await self.fetch(query='SELECT * FROM users')
        
    async def login_user(self, login: OAuth2PasswordRequestForm = Depends()):                 
        user = await self.fetchrow('SELECT id, password FROM users WHERE login=($1)', login.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')                                                
        if not Hash.verify(user['password'], login.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect Password')
        access_token_expires = timedelta(minutes=cfg.tk_expire_minutes)      
        access_token = create_access_token(
            data={'sub': login.username, 'id': user['id']}, 
            expires_delta=access_token_expires
            )
        return {'access_token': access_token, 'token_type': 'bearer'}    

    async def remove_user_by_id(self, user_id: int):        
        if await self.execute('DELETE FROM users WHERE ID=($1)', user_id) == 'DELETE 0':
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'User with id {user_id} does not exist',
                    )
        else:
            return {'detail': f'User with id {user_id} is deleted'} 
