from fastapi import APIRouter
from app.endpoints import hotel, hotel_room, room_category, service

router = APIRouter()
router.include_router(hotel.router)
router.include_router(hotel_room.router)
router.include_router(room_category.router)
router.include_router(service.router)
