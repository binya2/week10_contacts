import os
from pathlib import Path
from .repositories.contact_sql import MySQLContactRepository
from .sql_connector import MySQLConnector, SQLConfig, init_db_from_file
from .. import DatabaseManager


def create_sql_db_manager(settings: dict) -> DatabaseManager:
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

    connector = MySQLConnector(
        host=conf.host, user=conf.user, password=conf.password,
        port=conf.port, database=conf.database, pool_size=conf.pool_size
    )

    return DatabaseManager(contacts=MySQLContactRepository(connector), _connector=connector)


__all__ = ["MySQLConnector", "MySQLContactRepository", "create_sql_db_manager"]
