from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.routes import router

import logging
from datetime import datetime

import app.sql_engine as database


from app.models.hotel import hotelModel
from app.models.hotel_room import roomModel

from app.dtos.hotelDtos import hotelRequestDto

from app.utils.tokenUtils import verify_token

router = APIRouter(
    prefix="/hotel",
    tags=["Hotel"],
    responses={404: {"description": "Not found"}},
)

db = database.get_db()

"""
CRUD Hotels
"""


@router.get("s", status_code=200)
async def get_all_hotels():
    result = db.query(hotelModel).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "name": r.name,
            "address": r.address,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("/{id}", status_code=200)
async def get_hotel(id: int):
    result = db.query(hotelModel).filter(hotelModel.id == id).first()
    if result is None:
        raise HTTPException(status_code=404)
    json_return = {
        "id": result.id,
        "name": result.name,
        "address": result.address,
        "phone_number": result.phone_number,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.post("", status_code=201)
async def add_hotel(
    hotelRequestDto: hotelRequestDto, authorized: bool = Depends(verify_token)
):
    logging.error(hotelRequestDto)
    result: hotelModel = hotelModel(
        name=hotelRequestDto.name,
        address=hotelRequestDto.address,
        phone_number=hotelRequestDto.phone_number,
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
        "address": result.address,
        "phone_number": result.phone_number,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.put("/{id}", status_code=200)
async def update_hotel(
    id: int,
    hotelRequestDto: hotelRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(hotelRequestDto)
    db.query(hotelModel).filter(hotelModel.id == id).update(
        {
            hotelModel.name: hotelRequestDto.name,
            hotelModel.address: hotelRequestDto.address,
            hotelModel.phone_number: hotelRequestDto.phone_number,
            hotelModel.updated_at: datetime.now(),
        }
    )
    db.commit()
    return "UPDATED"


@router.delete("/{id}", status_code=200)
async def delete_hotel(id: int, authorized: bool = Depends(verify_token)):
    result = db.get(hotelModel, id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
