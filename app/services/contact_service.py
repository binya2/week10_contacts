from typing import List

from bson import ObjectId
from db.Idatabase import IContactRepository
from models import ContactUpdate, Contact

from models.types import AbstractID


class ContactService:
    def __init__(self, repo: IContactRepository):
        self.repo = repo

    async def add_contact(self, contact: Contact) -> str:
        return await self.repo.create(contact)

    async def get_all_contacts(self) -> List[Contact]:
        return await self.repo.get_all()

    async def get_contact(self, contact_id:AbstractID) -> Contact:
        return await self.repo.get_by_id(contact_id)

    async def update_contact_details(self, contact_id: AbstractID, contact: ContactUpdate) -> None:
        await self.repo.update(contact_id, contact)

    async def remove_contact(self, contact_id:  int | ObjectId) -> None:
        await self.repo.delete(contact_id)
