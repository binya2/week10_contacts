from typing import List, Optional

from db.mySql.sql_data_interactor import MySQLConnector
from models import Contact

TABLE_NAME = "contacts"


class MySQLContactRepository:
    def __init__(self, db: MySQLConnector):
        self.db = db

    def create_contact(self, contact: Contact) -> int:
        query = (f"INSERT INTO contacts (first_name, last_name, phone_number)"
                 f"VALUES ('{contact.first_name}','{contact.last_name}','{contact.phone_number}')")
        with self.db.get_cursor() as cursor:
            cursor.execute(query)
            if cursor.rowcount != 1:
                raise Exception("Insert failed")
            return cursor.lastrowid

    def get_all_contacts(self) -> List[Contact]:
        query = f"SELECT * FROM contacts"
        with self.db.get_cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        return [
            Contact(
                id=row["id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                phone_number=row["phone_number"],
            )
            for row in rows
        ]

    def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        query = f"SELECT * FROM contacts WHERE id = {contact_id}"
        with self.db.get_cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        if row is None:
            return None

        return Contact(
            id=row["id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            phone_number=row["phone_number"],
        )

    def update_contact(self, contact: Contact):
        query = f"UPDATE contacts SET phone_number={contact.phone_number} WHERE id = {contact.id}"

        with self.db.get_cursor() as cursor:
            cursor.execute(query)
            if cursor.rowcount != 1:
                raise Exception("Update failed")

    def delete_contact(self, id: int):
        query = f"DELETE FROM contacts WHERE id = {id} "
        with self.db.get_cursor() as cursor:
            cursor.execute(query)
            if cursor.rowcount != 1:
                raise Exception("Delete failed")
