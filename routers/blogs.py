from typing import Optional

from fastapi import APIRouter, Depends

from managers.blog import Blog, BlogManager
from dependencies import get_blog_manager


router = APIRouter(prefix="/blogs")


@router.get('', tags=['Blogs'])
async def get_blogs(bm: BlogManager = Depends(get_blog_manager)):
    return await bm.get_blogs()


@router.post('', tags=['Blogs'])
async def create_blog(blog: Blog, bm: BlogManager = Depends(get_blog_manager)):
    await bm.add_blog(blog)


@router.delete('/{blog_id}', tags=['Blogs'])
async def delete_blog(blog_id: int, bm: BlogManager = Depends(get_blog_manager)):
    await bm.remove_blog_by_id(blog_id)


@router.get('/{blog_id}', tags=['Blogs'])
async def get_blog_by_id(blog_id: int, bm: BlogManager = Depends(get_blog_manager)) -> Optional[Blog]:
    return await bm.get_blog_by_id(blog_id)
    