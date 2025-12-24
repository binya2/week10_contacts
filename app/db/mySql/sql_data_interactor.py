import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import mysql.connector
from mysql.connector import Error as MySQLError

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent


class MySQLConnector:
    def __init__(
            self,
            host: str,
            user: str,
            password: Optional[str] = None,
            database: Optional[str] = None,
            sql_file: Optional[str] = None,
            charset: str = "utf8mb4",
    ):

        self.config = {
            "host": host,
            "user": user,
            "database": database,
            "password": password,
            "charset": charset,
        }

        self.connection = None
        self._connect()

        logger.info("Connection to MySQL DB successful")

        if sql_file:
            sql_path = Path(__file__).resolve().parent / "init.sql"
            self.init_database(sql_path)

    def _connect(self) -> None:
        try:
            self.connection = mysql.connector.connect(**self.config)
            if not self.connection.is_connected():
                raise RuntimeError("Connection object created but not connected")
        except MySQLError as err:
            logger.error(f"Failed to connect to MySQL: {err}")
            raise RuntimeError("Connection to MySQL DB failed") from err

    def _ensure_connection(self) -> None:
        if self.connection is None:
            self._connect()
            return

        if not self.connection.is_connected():
            try:
                self.connection.reconnect(attempts=3, delay=2)
            except MySQLError:
                logger.warning("Reconnect failed, creating new connection")
                self._connect()

    def __enter__(self) -> "MySQLConnector":
        self._ensure_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    @contextmanager
    def get_cursor(self):
        self._ensure_connection()
        assert self.connection is not None
        cursor = self.connection.cursor(dictionary=True)
        try:
            yield cursor
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def init_database(self, sql_file: str) -> None:
        with open(sql_file, "r", encoding="utf-8") as f:
            sql_script = f.read()
        commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]
        with self.get_cursor() as cursor:
            for command in commands:
                try:
                    cursor.execute(command)
                except MySQLError as err:
                    logger.error(f"Command error:\n{command}\n{err}")

    def close(self) -> None:
        if self.connection is not None:
            if self.connection.is_connected():
                self.connection.close()
            self.connection = None
