from abc import ABC, abstractmethod
from typing import List, Optional

from bson import ObjectId
from models import ContactUpdate, Contact


class BaseRepository:
    def __init__(self, connector):
        self.connector = connector


class IContactRepository(ABC):
    @abstractmethod
    def create(self, contact: Contact) -> str:
        pass

    @abstractmethod
    def get_all(self) -> List[Contact]:
        pass

    @abstractmethod
    def get_by_id(self, contact_id: int | ObjectId) -> Optional[Contact]:
        pass

    @abstractmethod
    def update(self, contact_id: int | ObjectId, contact: ContactUpdate) -> None:
        pass

    @abstractmethod
    def delete(self, contact_id: int) -> None:
        pass
