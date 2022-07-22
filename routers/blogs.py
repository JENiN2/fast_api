from typing import Optional

from fastapi import APIRouter, Depends

from managers.blog import Blog, BlogManager
from dependencies import get_blog_manager
from oauth2 import get_current_user
import schemas


router = APIRouter(prefix="/blogs")


@router.get('', tags=['Blogs'])
async def get_blogs(bm: BlogManager = Depends(get_blog_manager),
    get_current_user: schemas.User = Depends(get_current_user)
    ):    
    return await bm.get_blogs()


@router.post('', tags=['Blogs'])
async def create_blog(blog: Blog, bm: BlogManager = Depends(get_blog_manager), 
    get_current_user: schemas.User = Depends(get_current_user),        
    ):    
    await bm.add_blog(blog, get_current_user)


@router.delete('/{blog_id}', tags=['Blogs'])
async def delete_blog(blog_id: int, bm: BlogManager = Depends(get_blog_manager), get_current_user: schemas.User = Depends(get_current_user)):
    await bm.remove_blog_by_id(blog_id)


@router.get('/{blog_id}', tags=['Blogs'])
async def get_blog_by_id(blog_id: int, bm: BlogManager = Depends(get_blog_manager), get_current_user: schemas.User = Depends(get_current_user)) -> Optional[Blog]:
    return await bm.get_blog_by_id(blog_id)
    