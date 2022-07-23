from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from managers.user import UserManager
from dependencies import get_user_manager

from jose import jwt, JWTError
from schemas import TokenData, User
from config import Config


cfg = Config()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='Users/login')


async def get_current_user(token: str = Depends(oauth2_scheme), um: UserManager = Depends(get_user_manager)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, cfg.tk_secret_key, algorithms=[cfg.tk_algorithm])
        login: str = payload.get('sub')
        if login is None:
            raise credentials_exception
        token_data = TokenData(login=login) 
    except JWTError:
        raise credentials_exception
    user_id: User = payload.get('id')
    if user_id is None:
        raise credentials_exception    
    return user_id
