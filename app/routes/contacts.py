from fastapi import APIRouter

router = APIRouter(tags=["contacts"])


@router.post("/contacts")
async def post_contacts():

    return {"message": "contact added"}


@router.put("/contacts")
async def put_contacts():
    return {"message": "contact added"}


@router.get("/contacts")
async def get_contacts():
    return {"message": "contact added"}


@router.delete("/contacts")
async def delete_contacts():
    return {"message": "contact deleted"}
