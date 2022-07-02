from fastapi import FastAPI
import uvicorn
import asyncpg

from routers.blogs import router as blog_router
from routers.users import router as user_router
from config import Config

app = FastAPI()
cfg = Config()


@app.on_event('startup')
async def startup():
    app.state.pg_pool = await asyncpg.create_pool(
        f'postgres://{cfg.pg_user}:{cfg.pg_password}@{cfg.pg_host}:{cfg.pg_port}/{cfg.pg_db}',
        min_size=cfg.pg_pool_min_size,
        max_size=cfg.pg_pool_max_size
    )  


app.include_router(blog_router)
app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=cfg.app_server_host,
        port=cfg.app_server_port
    )
