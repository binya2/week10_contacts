from typing import Optional
from .manager import DatabaseManager
from .factory import get_db_manager
from .exceptions import *

_db_instance: Optional[DatabaseManager] = None

def get_db() -> DatabaseManager:
    global _db_instance
    if _db_instance is None:
        _db_instance = get_db_manager()
    return _db_instance

def reload_db():
    global _db_instance
    _db_instance = None
    get_db()

__all__ = ["get_db", "reload_db", "DatabaseManager"]