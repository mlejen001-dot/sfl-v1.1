import sqlite3
from contextlib import contextmanager


class Database:
    def __init__(self, db_path="flower.db"):
        self.db_path = db_path

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def fetch_one(self, query, params=()):
        with self.connection() as conn:
            return conn.execute(query, params).fetchone()

    def fetch_all(self, query, params=()):
        with self.connection() as conn:
            return conn.execute(query, params).fetchall()
