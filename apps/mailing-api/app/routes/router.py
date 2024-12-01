from fastapi import APIRouter
from app.endpoints import mail

router = APIRouter()
router.include_router(mail.router)
