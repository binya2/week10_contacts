from typing import List

from db.Idatabase import IContactRepository
from models import Contact
from starlette.concurrency import run_in_threadpool


class ContactService:
    def __init__(self, repo: IContactRepository):
        self.repo = repo

    async def add_contact(self, contact: Contact) -> int:
        return await run_in_threadpool(self.repo.contacts.create, contact)

    async def get_contacts(self) -> List[Contact]:
        return await run_in_threadpool(self.repo.contacts.get_all)

    async def get_contact(self, contact_id: int) -> Contact:
        return await run_in_threadpool(self.repo.contacts.get_by_id, contact_id)

    async def update_contact_details(self, contact: Contact) -> None:
        await run_in_threadpool(self.repo.contacts.update, contact)

    async def remove_contact(self, contact_id: int) -> None:
        await run_in_threadpool(self.repo.contacts.delete, contact_id)
