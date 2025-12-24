from abc import ABC, abstractmethod
from typing import List, Optional

from models import Contact


class BaseRepository:
    def __init__(self, connector):
        self.connector = connector


class IContactRepository(ABC):
    @abstractmethod
    def create(self, contact: Contact) -> int:
        pass

    @abstractmethod
    def get_all(self) -> List[Contact]:
        pass

    @abstractmethod
    def get_by_id(self, contact_id: int) -> Optional[Contact]:
        pass

    @abstractmethod
    def update(self, contact: Contact) -> None:
        pass

    @abstractmethod
    def delete(self, contact_id: int) -> None:
        pass
