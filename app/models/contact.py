from typing import Optional

from models.types import AbstractID
from pydantic import BaseModel, Field, ConfigDict


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


class Contact(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        from_attributes=True
    )
    id: Optional[AbstractID] = Field(default=None, alias="_id")
    first_name: str
    last_name: str
    phone_number: str
