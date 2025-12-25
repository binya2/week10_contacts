import traceback

from db import get_db
from db.exceptions import OperationFailed, RecordNotFound
from db.manager import DatabaseManager
from fastapi import APIRouter, Depends, HTTPException
from services.contact_service import ContactService
from starlette import status

from models import ContactIn, ContactPhoneNumber, Contact


router = APIRouter(tags=["contacts_api"])


def get_service(db: DatabaseManager = Depends(get_db)) -> ContactService:
    return ContactService(db.contacts)


@router.post("/contacts", status_code=status.HTTP_201_CREATED)
async def post_contacts(
        contact_in: ContactIn,
        service: ContactService = Depends(get_service)
):
    try:
        new_id = await service.add_contact(contact_in)
        contact = Contact(id=new_id,
                          phone_number=contact_in.phone_number,
                          first_name=contact_in.first_name,
                          last_name=contact_in.last_name)
        return {
            "message": "contact added",
            "new_contact": contact
        }
    except OperationFailed:
        raise HTTPException(status_code=500, detail="Internal Database Error")
    except Exception as e:
        print("ERROR IN POST:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/contacts/{contact_id}")
async def put_contacts(
        contact_id: int,
        phone_payload: ContactPhoneNumber,
        service: ContactService = Depends(get_service)
):
    try:
        contact = await service.get_contact(contact_id)

        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")

        contact.phone_number = phone_payload.phone_number

        await service.update_contact_details(contact)
        return {"message": "contact updated successfully"}

    except RecordNotFound:
        raise HTTPException(status_code=404, detail="Contact not found")
    except OperationFailed:
        raise HTTPException(status_code=500, detail="Database update failed")


@router.get("/contacts")
async def get_contacts(service: ContactService = Depends(get_service)):
    try:
        contacts = await service.get_all_contacts()
        return {"list_of_all_contacts": contacts}
    except OperationFailed:
        raise HTTPException(status_code=500, detail="Failed to retrieve contacts")


@router.delete("/contacts/{contact_id}")
async def delete_contacts(
        contact_id: int,
        service: ContactService = Depends(get_service)
):
    try:
        await service.remove_contact(contact_id)
        return {"message": "contact deleted successfully"}
    except RecordNotFound:
        raise HTTPException(status_code=404, detail="Contact not found")
    except OperationFailed:
        raise HTTPException(status_code=500, detail="Failed to delete contact")
