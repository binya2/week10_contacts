
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from db.Idatabase import IContactRepository
from db.sql_repository import MySQLContactRepository, MySQLConnector

from db.sql_repository.sql_connector import DBConfig


@dataclass
class DatabaseManager:
    contacts: IContactRepository
    _connector: Optional[object] = None

    async def close(self):
        if hasattr(self._connector, "close"):
            self._connector.close()

    @classmethod
    def create_mysql(cls, config: DBConfig):
        print(f"Connecting to MySQL at {config.host}...")

        connector = MySQLConnector(
            host=config.host,
            user=config.user,
            password=config.password,
            port=config.port,
            database=config.database,
            pool_size=config.pool_size
        )

        try:
            base_dir = Path(__file__).parent
            sql_path = base_dir / "sql_repository" / "init.sql"

            if sql_path.exists():
                with open(sql_path, "r") as f:
                    sql_script = f.read()

                commands = sql_script.split(';')
                with connector.get_cursor() as cursor:
                    for command in commands:
                        if command.strip():
                            try:
                                cursor.execute(command)
                            except:
                                pass
        except Exception as e:
            print(f"Note: Schema init skipped or failed: {e}")

        return cls(
            contacts=MySQLContactRepository(connector),
            _connector=connector
        )
