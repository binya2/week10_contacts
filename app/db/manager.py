from dataclasses import dataclass
from typing import Optional
from .Idatabase import IContactRepository

@dataclass
class DatabaseManager:
    contacts: IContactRepository
    _connector: Optional[object] = None

    async def close(self):
        if hasattr(self._connector, "close"):
            self._connector.close()