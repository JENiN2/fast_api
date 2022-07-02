from abc import ABC

from .dbmixin import DBMixin

class BaseManager(ABC, DBMixin):
    def __init__(self, pg) -> None:
        self.pg = pg
