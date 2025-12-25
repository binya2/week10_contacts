from db import get_db
from db.exceptions import OperationFailed, RecordNotFound
from db.manager import DatabaseManager
from fastapi import APIRouter, Depends, HTTPException
from models import ContactIn, ContactPhoneNumber, Contact
from services.contact_service import ContactService
from starlette import status

router = APIRouter(tags=["contacts_api"])


def get_service(db: DatabaseManager = Depends(get_db)) -> ContactService:
    return ContactService(db.contacts)


@router.post("/contacts", status_code=status.HTTP_201_CREATED)
async def post_contacts(contact_in: ContactIn, service: ContactService = Depends(get_service)):
    try:
        contact = await service.add_contact(contact_in)
        return {
            "message": "contact added",
            "new_contact": contact
        }
    except OperationFailed:
        raise HTTPException(status_code=500, detail="Internal Database Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/contacts/{contact_id}")
async def put_contacts(contact_id: int, contact_phone: ContactPhoneNumber,
                       service: ContactService = Depends(get_service)):
    try:
        await service.update_contact_details(contact_id, contact_phone)
        return {
            "message": "contact updated successfully"
        }
    except RecordNotFound as e:
        raise HTTPException(status_code=404, detail=f"Contact not found:\n{e}") from e
    except OperationFailed:
        raise HTTPException(status_code=500, detail="Database update failed")


@router.get("/contacts")
async def get_contacts(service: ContactService = Depends(get_service)):
    try:
        contacts = await service.get_all_contacts()
        return {
            "list_of_all_contacts": contacts
        }
    except OperationFailed:
        raise HTTPException(status_code=500, detail="Failed to retrieve contacts")


@router.delete("/contacts/{contact_id}")
async def delete_contacts(contact_id: int, service: ContactService = Depends(get_service)):
    try:
        await service.remove_contact(contact_id)
        return {
            "message": "contact deleted successfully"
        }
    except RecordNotFound as e:
        raise HTTPException(status_code=404, detail=f"Contact not found:\n{e}") from e
    except OperationFailed:
        raise HTTPException(status_code=500, detail="Failed to delete contact")
