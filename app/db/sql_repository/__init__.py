import os
from pathlib import Path

from db.manager import DatabaseManager

from .repositories.contact_sql import MySQLContactRepository
from .sql_connector import MySQLConnector, SQLConfig, init_db_from_file


def create_sql_db_manager(settings: dict) -> DatabaseManager:
    """Creates and returns a DatabaseManager for MySQL."""
    if os.getenv("DB_HOST"): settings["host"] = os.getenv("DB_HOST")
    if os.getenv("DB_USER"): settings["user"] = os.getenv("DB_USER")
    if os.getenv("DB_PASSWORD"): settings["password"] = os.getenv("DB_PASSWORD")

    conf = SQLConfig(**settings)
    print(f"Factory: Connecting to SQL host: {conf.host}...")

    try:
        base_dir = Path(__file__).resolve().parent
        sql_path = base_dir / "init.sql"
        real_db_name = init_db_from_file(conf, str(sql_path))
        conf.database = real_db_name
    except Exception as e:
        print(f"Bootstrap Warning: {e}")

    connector = MySQLConnector(conf)

    return DatabaseManager(contacts=MySQLContactRepository(connector), _connector=connector)


__all__ = ["MySQLConnector", "MySQLContactRepository", "create_sql_db_manager"]
