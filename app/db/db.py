from app.db.mySql.contact_sql import MySQLContactRepository
from app.db.mySql.sql_data_interactor import MySQLConnector

db_connector = MySQLConnector(
    host="localhost",
    user="root",
    password="Benny31.",
    sql_file=r"C:\KodkodData\week_10\week10_contacts\app\db\mySql\init.sql",
)


def get_contact_repository() -> MySQLContactRepository:
    return MySQLContactRepository(db_connector)
