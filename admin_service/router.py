from fastapi import APIRouter, Depends

from deps import get_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get("/")
async def start_admin(
    admin_current_user=Depends(get_admin_user),
):
    return admin_current_user
