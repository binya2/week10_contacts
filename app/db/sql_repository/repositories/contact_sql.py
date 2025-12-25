from typing import List, Optional

from db.Idatabase import BaseRepository, IContactRepository
from db.exceptions import OperationFailed, RecordNotFound
from mysql.connector import Error as MySQLError

from models import Contact, ContactIn, ContactPhoneNumber


class MySQLContactRepository(BaseRepository, IContactRepository):

    def create(self, contact: ContactIn) -> int:
        query = "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)"
        params = (contact.first_name, contact.last_name, contact.phone_number)
        try:
            with self.connector.get_cursor() as cursor:
                cursor.execute(query, params)
                new_id = cursor.lastrowid
            return self.get_by_id(new_id)
        except MySQLError as e:
            raise OperationFailed(f"Create failed: {e}") from e

    def get_all(self) -> List[Contact]:
        query = "SELECT * FROM contacts"
        with self.connector.get_cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return [Contact(**row) for row in rows]

    def get_by_id(self, contact_id: int) -> Optional[Contact]:
        query = "SELECT * FROM contacts WHERE id = %s"
        with self.connector.get_cursor() as cursor:
            cursor.execute(query, (contact_id,))
            row = cursor.fetchone()
            print(cursor.fetchone())
            if row:
                return Contact(**row)
            return None

    def update(self, contact_id: int, contact_phone: ContactPhoneNumber) -> None:
        contact = self.get_by_id(contact_id)
        if not contact:
            raise RecordNotFound("Cannot update contact without ID")

        query = "UPDATE contacts SET phone_number=%s WHERE id=%s"
        params = (contact_phone.phone_number, contact.id)

        try:
            with self.connector.get_cursor() as cursor:
                cursor.execute(query, params)
        except MySQLError as e:
            raise OperationFailed(f"Update failed: {e}") from e

    def delete(self, contact_id: int) -> None:
        query = "DELETE FROM contacts WHERE id = %s"
        with self.connector.get_cursor() as cursor:
            cursor.execute(query, (contact_id,))
            if cursor.rowcount == 0:
                raise RecordNotFound(f"Contact {contact_id} not found")
