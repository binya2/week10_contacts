from typing import List

from bson import ObjectId
from db.Idatabase import IContactRepository
from models import ContactUpdate, Contact
from starlette.concurrency import run_in_threadpool


class ContactService:
    def __init__(self, repo: IContactRepository):
        """Service layer for managing contacts."""
        self.repo = repo

    async def add_contact(self, contact: Contact) -> str:
        """Adds a new contact to the repository."""
        return await run_in_threadpool(self.repo.create, contact)


    async def get_all_contacts(self) -> List[Contact]:
        """Retrieves all contacts from the repository."""
        return await run_in_threadpool(self.repo.get_all)

    async def update_contact_details(self, contact_id: str, contact: ContactUpdate) -> None:
        """Updates the details of an existing contact."""
        await run_in_threadpool(self.repo.update, contact_id, contact)

    async def remove_contact(self, contact_id: str | ObjectId) -> None:
        """Removes a contact from the repository."""
        await run_in_threadpool(self.repo.delete, contact_id)
