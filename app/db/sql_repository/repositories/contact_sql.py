from typing import List, Optional

from db.Idatabase import BaseRepository, IContactRepository
from db.exceptions import OperationFailed, RecordNotFound
from models import Contact, ContactUpdate
from mysql.connector import Error as MySQLError
from starlette.concurrency import run_in_threadpool


class MySQLContactRepository(BaseRepository, IContactRepository):

    def _create_sync(self, contact: Contact) -> str:
        query = "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)"
        params = (contact.first_name, contact.last_name, contact.phone_number)
        try:
            with self.connector.get_cursor() as cursor:
                cursor.execute(query, params)
                return str(cursor.lastrowid)

        except MySQLError as e:
            raise OperationFailed(f"Create failed: {e}") from e

    def _get_all_sync(self) -> List[Contact]:
        query = "SELECT * FROM contacts"
        with self.connector.get_cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return [Contact(**row) for row in rows]

    def _get_by_id_sync(self, contact_id: int) -> Optional[Contact]:
        query = "SELECT * FROM contacts WHERE id = %s"
        with self.connector.get_cursor() as cursor:
            cursor.execute(query, (contact_id,))
            row = cursor.fetchone()
            if row:
                return Contact(**row)
            return None

    def _update_sync(self, contact_id: int, contact_update: ContactUpdate) -> None:
        updates = []
        params = []

        if contact_update.first_name is not None:
            updates.append("first_name = %s")
            params.append(contact_update.first_name)
        if contact_update.last_name is not None:
            updates.append("last_name = %s")
            params.append(contact_update.last_name)
        if contact_update.phone_number is not None:
            updates.append("phone_number = %s")
            params.append(contact_update.phone_number)
        if not updates:
            return

        params.append(contact_id)
        set_clause = ", ".join(updates)
        query = f"UPDATE contacts SET {set_clause} WHERE id = %s"

        try:
            with self.connector.get_cursor() as cursor:
                cursor.execute(query, tuple(params))
        except MySQLError as e:
            raise OperationFailed(f"Update failed: {e}") from e

    def _delete_sync(self, contact_id: int) -> None:
        query = "DELETE FROM contacts WHERE id = %s"
        with self.connector.get_cursor() as cursor:
            cursor.execute(query, (contact_id,))
            if cursor.rowcount == 0:
                raise RecordNotFound(f"Contact {contact_id} not found")

    async def create(self, contact: Contact) -> str:
        return await run_in_threadpool(self._create_sync, contact)

    async def get_all(self) -> List[Contact]:
        return await run_in_threadpool(self._get_all_sync)

    async def get_by_id(self, contact_id: int) -> Optional[Contact]:
        return await run_in_threadpool(self._get_by_id_sync, contact_id)

    async def update(self, contact_id: int, contact: ContactUpdate) -> None:
        await run_in_threadpool(self._update_sync, contact_id, contact)

    async def delete(self, contact_id: int) -> None:
        await run_in_threadpool(self._delete_sync, contact_id)
