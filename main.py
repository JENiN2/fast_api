from asyncore import read
import os.path
import json

from fastapi import FastAPI

from blog_manager import Blog, BlogManager

app = FastAPI()
app.state.blog_manager = BlogManager()

@app.on_event("startup")
async def startup_event():
    if not os.path.isfile('data.json'):
        return
    with open('data.json', 'r') as f:
        file = f.read()
        parsed_data = json.loads(file)
        app.state.blog_manager.storage = [Blog(**blog) for blog in parsed_data]
        # for blog in parsed_data:
        #     app.state.blog_manager.add_blog(Blog(**blog))

@app.on_event('shutdown')
async def shutdown_event():
    if not app.state.blog_manager.storage:
        return
    data = [blog.dict() for blog in app.state.blog_manager.storage]
    with open('data.json', 'w') as f:
        json.dump(data, f)

@app.get('/blogs')
def get_blogs():
    return app.state.blog_manager.storage

@app.post('/blogs')
def create_blog(blog: Blog):
    app.state.blog_manager.add_blog(blog)

@app.delete('/blogs/{blog_id}')
def delete_blog(blog_id: int):
    app.state.blog_manager.remove_blog_by_id(blog_id)
