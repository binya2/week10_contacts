from fastapi import APIRouter, Depends, HTTPException

from db.db import get_contact_repository
from db.mySql.contact_sql import MySQLContactRepository
from models import Contact

router = APIRouter(tags=["contacts_api"])


@router.post("/contacts")
async def post_contacts(contact_in: Contact, repo: MySQLContactRepository = Depends(get_contact_repository)):
    contact_in.id = repo.create_contact(contact_in)
    return {
        "message": "contact added",
        "new contact": contact_in
    }


@router.put("/contacts/{contact_id}")
async def put_contacts(contact_id: int, phone_number: dict,
                       repo: MySQLContactRepository = Depends(get_contact_repository)):
    updated_contact = repo.get_contact_by_id(contact_id)

    if updated_contact is None:
        return {"message": "contact no found"}

    updated_contact.phone_number = phone_number["phone_number"]
    try:
        repo.update_contact(updated_contact)
    except Exception:
        return {"message": "No changes found"}
    return {"message": "contact updated successfully"}


@router.get("/contacts")
async def get_contacts(repo: MySQLContactRepository = Depends(get_contact_repository)):
    contacts = repo.get_all_contacts()
    return {"list of al contacts": contacts}


@router.delete("/contacts/{contact_id}")
async def delete_contacts(contact_id: int,
                          repo: MySQLContactRepository = Depends(get_contact_repository)):
    try:
        repo.delete_contact(contact_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Contact not found")

    return {"message": "contact deleted successfully"}
