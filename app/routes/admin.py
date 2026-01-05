from fastapi import APIRouter, HTTPException, Depends
from services.admin_service import AdminService
from starlette import status

router = APIRouter(tags=["admin"])


def get_admin_service() -> AdminService:
    """Dependency injector for AdminService."""
    return AdminService()


@router.post("/admin/reload-db")
async def reload_database_config(service: AdminService = Depends(get_admin_service)):
    """Endpoint to reload the database configuration from config.json."""
    try:
        service.reload_system_config()

        return {"message": "Database configuration reloaded successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reload DB: {str(e)}"
        )
