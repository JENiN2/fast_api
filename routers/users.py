from fastapi import APIRouter, Depends

from managers.user import UserManager, User
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import get_user_manager


router = APIRouter(prefix="/Users")


@router.post('/register/', tags=['Users'])
async def register_user(user: User, um: UserManager = Depends(get_user_manager)):
    return await um.add_user(user)


@router.post('/login/', tags=['Users'])
async def login_user(login: OAuth2PasswordRequestForm = Depends(), um: UserManager = Depends(get_user_manager)):
    return await um.login_user(login)


@router.get('/users/', tags=['Users'])
async def get_users(um: UserManager = Depends(get_user_manager)):
    return await um.get_users()


@router.delete('/users/{user_id}', tags=['Users'])
async def delete_user(user_id: int, um: UserManager = Depends(get_user_manager)):
    return await um.remove_user_by_id(user_id)