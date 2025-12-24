from typing import List

from db.Idatabase import IContactRepository
from models import Contact


class ContactService:
    def __init__(self, repo: IContactRepository):
        self.repo = repo

    async def add_contact(self, contact: Contact) -> int:
        new_id = await self.repo.create(contact)
        return new_id

    async def get_contacts(self) -> List[Contact]:
        return await self.repo.get_all()

    async def get_contact(self, contact_id: int) -> Contact:
        return await self.repo.get_by_id(contact_id)

    async def update_contact_details(self, contact: Contact) -> None:
        await self.repo.update(contact)

    async def remove_contact(self, contact_id: int) -> None:
        await self.repo.delete(contact_id)