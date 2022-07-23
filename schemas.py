from typing import Optional

from pydantic import BaseModel

class Blog(BaseModel):
    id: Optional[int] = None
    title: str
    body: str
    created: str
    published: bool
    user_id: int    
   

class User(BaseModel):
    id: Optional[int] = None
    login: str
    first_name: str
    last_name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: str | None = None
