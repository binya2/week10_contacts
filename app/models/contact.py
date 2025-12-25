from pydantic import BaseModel


class ContactPhoneNumber(BaseModel):
    phone_number: str


class ContactIn(ContactPhoneNumber):
    first_name: str
    last_name: str


class Contact(ContactIn):
    id: int
