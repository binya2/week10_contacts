from typing import List, Optional

from app.db.mySql.sql_data_interactor import MySQLConnector
from app.models import Contact


class MySQLContactRepository:
    def __init__(self, db: MySQLConnector):
        self.db = db

    def create_contact(self, contact: Contact) -> int:
        query = """
                INSERT INTO contact (first_name, last_name, phone_number)
                VALUES (%s, %s, %s)
                """
        values = (
            contact.first_name,
            contact.last_name,
            contact.phone_number,
        )
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
            if cursor.rowcount != 1:
                raise Exception("Insert failed")
            return cursor.lastrowid

    def get_all_contacts(self) -> List[Contact]:
        query = "SELECT * FROM contact"
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
        query = "SELECT * FROM contact WHERE id = %s"
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (contact_id,))
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
        query = """
                UPDATE contact
                SET first_name=%s,
                    last_name=%s,
                    phone_number=%s
                WHERE id = %s
                """
        values = (
            contact.first_name,
            contact.last_name,
            contact.phone_number,
            contact.id,
        )
        with self.db.get_cursor() as cursor:
            cursor.execute(query, values)
            if cursor.rowcount != 1:
                raise Exception("Update failed")

    def delete_contact(self, id: int):
        query = """
                DELETE
                FROM contact
                WHERE id = %s
                """
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (id,))
            if cursor.rowcount != 1:
                raise Exception("Delete failed")
