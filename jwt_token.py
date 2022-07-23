from datetime import datetime, timedelta

from jose import jwt

from config import Config


cfg = Config()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=cfg.tk_expire_minutes)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, cfg.tk_secret_key, algorithm=cfg.tk_algorithm)
    return encoded_jwt
