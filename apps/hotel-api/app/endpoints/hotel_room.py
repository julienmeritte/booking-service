from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.routes import router

import logging
from datetime import datetime

import app.sql_engine as database


from app.models.hotel_room import roomModel

from app.dtos.hotelRoomCategoryDtos import hotelRoomRequestDto

from app.utils.tokenUtils import verify_token

from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/room",
    tags=["HotelRooms"],
    responses={404: {"description": "Not found"}},
)

db = database.get_db()


"""
CRUD Rooms
"""


@router.get("s", status_code=200)
async def get_all_rooms():
    result = db.query(roomModel).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "hotel_id": r.hotel_id,
            "room_number": r.room_number,
            "category_id": r.category_id,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("s/hotel/{hotel_id}", status_code=200)
async def get_all_rooms_by_Hotel(hotel_id: int):
    result = db.query(roomModel).filter(roomModel.hotel_id == hotel_id).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "hotel_id": r.hotel_id,
            "room_number": r.room_number,
            "category_id": r.category_id,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("/{room_id}", status_code=200)
async def get_room(room_id: int):
    result = db.query(roomModel).filter(roomModel.id == room_id).first()

    if result is None:
        raise HTTPException(status_code=404)

    json_return = {
        "id": result.id,
        "hotel_id": result.hotel_id,
        "room_number": result.room_number,
        "category_id": result.category_id,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.post("", status_code=201)
async def add_Room(
    hotelRoomRequestDto: hotelRoomRequestDto, authorized: bool = Depends(verify_token)
):
    result: roomModel = roomModel(
        hotel_id=hotelRoomRequestDto.hotel_id,
        room_number=hotelRoomRequestDto.room_number,
        category_id=hotelRoomRequestDto.category_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    if result is None:
        raise HTTPException(status_code=500)

    try:
        db.add(result)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)

    json_return = {
        "id": result.id,
        "hotel_id": result.hotel_id,
        "room_number": result.room_number,
        "category_id": result.category_id,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.put("/{room_id}", status_code=200)
async def update_room(
    room_id: int,
    hotelRoomRequestDto: hotelRoomRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(hotelRoomRequestDto)

    try:
        db.query(roomModel).filter(roomModel.id == room_id).update(
            {
                roomModel.hotel_id: hotelRoomRequestDto.hotel_id,
                roomModel.room_number: hotelRoomRequestDto.room_number,
                roomModel.category_id: hotelRoomRequestDto.category_id,
                roomModel.updated_at: datetime.now(),
            }
        )
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)

    return "UPDATED"


@router.delete("/{id}", status_code=200)
async def delete_room(id: int, authorized: bool = Depends(verify_token)):
    result = db.get(roomModel, id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
