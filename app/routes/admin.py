from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from services.admin_service import AdminService

router = APIRouter(tags=["admin"])


def get_admin_service() -> AdminService:
    return AdminService()


@router.post("/admin/reload-db")
async def reload_database_config(service: AdminService = Depends(get_admin_service)):
    try:
        service.reload_system_config()

        return {"message": "Database configuration reloaded successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reload DB: {str(e)}"
        )