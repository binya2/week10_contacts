from typing import Optional

from pydantic import BaseModel


class ContactUpdate(BaseModel):
    """Model for updating contact information."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


class Contact(BaseModel):
    """Model representing a contact."""
    id: Optional[str] = None
    first_name: str
    last_name: str
    phone_number: str
