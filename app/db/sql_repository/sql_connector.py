import os
import re
from contextlib import contextmanager
from dataclasses import dataclass

import mysql.connector


@dataclass
class SQLConfig:
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = ""
    database: str = "rolling_project"
    pool_size: int = 5


class MySQLConnector:
    def __init__(self, host, user, password, port, database, pool_size=5):
        self.db_config = {
            "host": host, "user": user, "password": password,
            "port": port, "database": database
        }
        self.pool_size = pool_size
        self._pool = None
        self._init_pool()

    def _init_pool(self):
        try:
            self._pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="mypool", pool_size=self.pool_size, **self.db_config
            )
        except Exception as e:
            raise e

    @contextmanager
    def get_cursor(self):
        conn = None
        cursor = None
        try:
            if not self._pool: self._init_pool()
            conn = self._pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            yield cursor
            conn.commit()
        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def close(self):
        pass


@contextmanager
def _server_connection(conf: SQLConfig):
    conn = mysql.connector.connect(
        host=conf.host, user=conf.user, password=conf.password, port=conf.port
    )
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def _extract_db_name(sql_text: str) -> str:
    match = re.search(r"CREATE\s+DATABASE\s+(?:IF\s+NOT\s+EXISTS\s+)?['`\"]?(\w+)['`\"]?", sql_text, re.IGNORECASE)
    if not match: raise ValueError("No 'CREATE DATABASE' found.")
    return match.group(1)


def _run_sql_commands(cursor, sql_text: str):
    for cmd in sql_text.split(';'):
        if cmd.strip(): cursor.execute(cmd.strip())


def init_db_from_file(conf: SQLConfig, file_path: str) -> str:
    if not os.path.exists(file_path): raise FileNotFoundError(f"Missing file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        script = f.read()

    db_name = _extract_db_name(script)
    print(f"Detected DB Name: {db_name}")

    with _server_connection(conf) as cursor:
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")

        if not cursor.fetchone():
            print(f"Creating database '{db_name}'...")
            _run_sql_commands(cursor, script)
            print("Database initialized successfully.")
        else:
            print("Database already exists.")

    return db_name
