import json
import logging
import os
from contextlib import contextmanager
from dataclasses import dataclass

from mysql.connector import pooling, Error as MySQLError

logger = logging.getLogger(__name__)


@dataclass
class DBConfig:
    host: str
    user: str
    password: str
    database: str
    port: int = 3306
    pool_size: int = 5
    db_type: str = "mysql"


def load_config(config_path: str = "config.json") -> DBConfig:
    config_values = {
        "host": "localhost",
        "user": "root",
        "password": "Benny31.",
        "database": "rolling_project",
        "pool_size": 5,
        "db_type": "mysql"
    }

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                file_data = json.load(f)
                active = file_data.get("active_db", "mysql")

                config_values["db_type"] = active

                db_data = file_data.get("connections", {}).get(active, {})
                config_values.update({k: v for k, v in db_data.items() if v is not None})
        except Exception as e:
            print(f"Warning: Failed to load config file: {e}")

    # דריסות Environment Variables
    config_values["host"] = os.getenv("DB_HOST", config_values["host"])
    config_values["user"] = os.getenv("DB_USER", config_values["user"])
    config_values["password"] = os.getenv("DB_PASSWORD", config_values["password"])
    config_values["database"] = os.getenv("DB_NAME", config_values["database"])

    pool_size_env = os.getenv("DB_POOL_SIZE")
    if pool_size_env:
        config_values["pool_size"] = int(pool_size_env)

    return DBConfig(**config_values)


class MySQLConnector:
    def __init__(self, host, user, password, port, database, pool_size=5):
        self.dbconfig = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "charset": "utf8mb4"
        }
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="api_pool",
                pool_size=pool_size,
                pool_reset_session=True,
                **self.dbconfig
            )
        except MySQLError as err:
            logger.error(f"Failed to create connection pool: {err}")
            raise RuntimeError("DB Pool creation failed") from err

    @contextmanager
    def get_cursor(self):
        connection = None
        cursor = None
        try:
            connection = self.pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            yield cursor
            connection.commit()
        except Exception:
            if connection:
                try:
                    connection.rollback()
                except:
                    pass
            raise
        finally:
            if cursor: cursor.close()
            if connection: connection.close()


