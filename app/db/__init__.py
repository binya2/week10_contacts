from typing import Optional

from db.exceptions import AppDatabaseError, RecordNotFound, OperationFailed
from db.manager import DatabaseManager
from db.sql_repository.sql_connector import load_config

_db_instance: Optional[DatabaseManager] = None


def get_db() -> DatabaseManager:
    global _db_instance
    if _db_instance is None:
        _initialize_db()
    return _db_instance


def _initialize_db():
    global _db_instance

    config = load_config()

    if config.db_type == "mysql":
        print("Initializing MySQL Manager...")
        _db_instance = DatabaseManager.create_mysql(config)

    elif config.db_type == "mongo":
        print("Initializing Mongo Manager...")
        raise NotImplementedError("Mongo not ready yet")

    else:
        raise ValueError(f"Unknown DB type: {config.db_type}")

    print("Database Initialized Successfully.")


def reload_db():
    global _db_instance
    print("Reloading Database Configuration...")
    if _db_instance:
        try:
            pass
        except:
            pass

    _db_instance = None
    _initialize_db()


__all__ = ["get_db", "reload_db", "DatabaseManager", "AppDatabaseError", "RecordNotFound", "OperationFailed"]
