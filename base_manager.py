from abc import ABC

from database_query import DBMixin

class BaseManager(ABC, DBMixin):
    def __init__(self, pool) -> None:
        self.pg = pool
        