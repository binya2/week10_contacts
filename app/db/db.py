from app.db.mySql.contact_sql import MySQLContactRepository
from app.db.mySql.sql_data_interactor import MySQLConnector

db_connector = MySQLConnector(
    host="localhost",
    user="root",
    password="secret",
)


def get_contact_repository() -> MySQLContactRepository:
    return MySQLContactRepository(db_connector)
