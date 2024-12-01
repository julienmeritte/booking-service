from fastapi import APIRouter
from app.endpoints import reservation, reservation_service, discount_type, discount

router = APIRouter()
router.include_router(reservation.router)
router.include_router(reservation_service.router)
router.include_router(discount_type.router)
router.include_router(discount.router)
