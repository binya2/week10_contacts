from abc import ABC, abstractmethod
from typing import List, Optional

from models import Contact


class BaseRepository:
    def __init__(self, connector):
        self.connector = connector


class IContactRepository(ABC):
    @abstractmethod
    async def create(self, contact: Contact) -> int:  # הוספנו async
        pass

    @abstractmethod
    async def get_all(self) -> List[Contact]:  # הוספנו async
        pass

    @abstractmethod
    async def get_by_id(self, contact_id: int) -> Optional[Contact]:
        pass

    @abstractmethod
    async def update(self, contact: Contact) -> None:
        pass

    @abstractmethod
    async def delete(self, contact_id: int) -> None:
        pass
