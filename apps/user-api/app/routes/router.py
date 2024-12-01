from fastapi import APIRouter
from app.endpoints import user, role, role_user

router = APIRouter()
router.include_router(user.router)
router.include_router(role.router)
router.include_router(role_user.router)
