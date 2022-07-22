from datetime import datetime, timedelta

from jose import jwt, JWTError

import schemas
from config import Config


cfg = Config()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=cfg.tk_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, cfg.tk_secret_key, algorithm=cfg.tk_algorithm)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, cfg.tk_secret_key, algorithms=[cfg.tk_algorithm])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
        token_data = schemas.TokenData(login=login)
    except JWTError:
        raise credentials_exception    
