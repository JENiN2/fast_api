from typing import Optional, List

from pydantic import BaseModel


class Blog(BaseModel):
    id: int
    title: str
    body: str
    published: Optional[bool]


class BlogManager:
    def __init__(self) -> None:
        self.storage: List[Blog] = []

    def add_blog(self, blog: Blog):
        self.storage.append(blog)
    
    def remove_blog_by_id(self, id: int):
        self.storage = [blog for blog in self.storage if blog.id != id]
