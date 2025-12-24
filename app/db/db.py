import os
from pathlib import Path

from mySql.contact_sql import MySQLContactRepository
from mySql.sql_data_interactor import MySQLConnector

BASE_DIR = Path(__file__).resolve().parent

db_connector = MySQLConnector(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "Benny31."),
    database=os.getenv("DB_NAME", "rolling_project"),
    sql_file=str(BASE_DIR / "mySql" / "init.sql"),
)


def get_contact_repository() -> MySQLContactRepository:
    return MySQLContactRepository(db_connector)
