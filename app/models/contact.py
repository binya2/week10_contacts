from typing import Optional

from pydantic import BaseModel


class Contact(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    phone_number: str

    def __dict__(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number
        }

class UpdateContactRequest(BaseModel):
    phone_number: str

    def __dict__(self):
        return {
            'phone_number': self.phone_number
        }