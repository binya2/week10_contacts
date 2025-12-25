from typing import List

from starlette.concurrency import run_in_threadpool

from db.Idatabase import IContactRepository
from models import ContactIn, Contact


class ContactService:
    def __init__(self, repo: IContactRepository):
        self.repo = repo

    async def add_contact(self, contact: ContactIn) -> int:
        return await run_in_threadpool(self.repo.create, contact)

    async def get_all_contacts(self) -> List[Contact]:
        return await run_in_threadpool(self.repo.get_all)

    async def get_contact(self, contact_id: int) -> Contact:
        return await run_in_threadpool(self.repo.get_by_id, contact_id)

    async def update_contact_details(self, contact: Contact) -> None:
        await run_in_threadpool(self.repo.update, contact)

    async def remove_contact(self, contact_id: int) -> None:
        await run_in_threadpool(self.repo.delete, contact_id)
