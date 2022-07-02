import asyncpg


class DBMixin():
    def __init__(self, pg):
        self.pg: asyncpg.Pool = pg

    async def execute(self, query, *args):
        async with self.pg.acquire() as conn:
            await conn.execute(query, *args)            
                            
    async def fetch(self, query, *args):
        async with self.pg.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pg.acquire() as conn:
            return await conn.fetchrow(query, *args)
