from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.routes import router

import logging
from datetime import datetime

import app.sql_engine as database

from app.models.room_category import roomCategoryModel

from app.dtos.roomCategoryDtos import roomCategoryRequestDto

from app.utils.tokenUtils import verify_token

router = APIRouter(
    prefix="/room-categor",
    tags=["RoomCategories"],
    responses={404: {"description": "Not found"}},
)

db = database.get_db()


"""
CRUD Room Categories
"""


@router.get("ies", status_code=200)
async def get_all_room_categories():
    result = db.query(roomCategoryModel).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "name": r.name,
            "max_occupancy": r.max_occupancy,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("y/{room_category_id}", status_code=200)
async def get_room_category(room_category_id: int):
    result = (
        db.query(roomCategoryModel)
        .filter(roomCategoryModel.id == room_category_id)
        .first()
    )
    if result is None:
        raise HTTPException(status_code=404)
    json_return = {
        "id": result.id,
        "name": result.name,
        "max_occupancy": result.max_occupancy,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.post("y", status_code=201)
async def add_room_category(
    roomCategoryRequestDto: roomCategoryRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(roomCategoryRequestDto)
    result: roomCategoryModel = roomCategoryModel(
        name=roomCategoryRequestDto.name,
        max_occupancy=roomCategoryRequestDto.max_occupancy,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    if result is None:
        raise HTTPException(status_code=500)
    db.add(result)
    db.commit()
    json_return = {
        "id": result.id,
        "name": result.name,
        "max_occupancy": result.max_occupancy,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.put("y/{room_category_id}", status_code=200)
async def update_room_category(
    room_category_id: int,
    roomCategoryRequestDto: roomCategoryRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(roomCategoryRequestDto)
    db.query(roomCategoryModel).filter(roomCategoryModel.id == room_category_id).update(
        {
            roomCategoryModel.name: roomCategoryRequestDto.name,
            roomCategoryModel.max_occupancy: roomCategoryRequestDto.max_occupancy,
            roomCategoryModel.updated_at: datetime.now(),
        }
    )
    db.commit()
    return "UPDATED"


@router.delete("y/{room_category_id}", status_code=200)
async def delete_room_category(
    room_category_id: int, authorized: bool = Depends(verify_token)
):
    result = db.get(roomCategoryModel, room_category_id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
