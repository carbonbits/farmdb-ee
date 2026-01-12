import duckdb
from typing import Optional

from settings import settings


class DB:
    _instance: Optional[duckdb.DuckDBPyConnection] = None

    @classmethod
    def connect(cls):
        if cls._instance is None:
            cls._instance = duckdb.connect(settings.database_path)

    @classmethod
    def disconnect(cls):
        if cls._instance:
            cls._instance.close()
            cls._instance = None

    @classmethod
    def get_connection(cls) -> duckdb.DuckDBPyConnection:
        if cls._instance is None:
            raise RuntimeError("Database is not connected. Call connect() first.")
        return cls._instance
    
    @classmethod
    def _initialize_database(cls):
        pass


def db() -> duckdb.DuckDBPyConnection:
    """
    Returns the shared database connection.
    """
    return DB.get_connection()
