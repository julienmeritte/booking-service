from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.routes import router
from app.models.reservation import reservationModel
from app.dtos.reservationDtos import reservationRequestDto

import app.sql_engine as database

from sqlalchemy.exc import IntegrityError

import logging

import os

import jwt
import bcrypt

from app.utils.tokenUtils import verify_token

router = APIRouter(
    prefix="/reservation",
    tags=["Reservation"],
    responses={404: {"description": "Not found"}},
)

"""
Routes pour Reservation
"""

db = database.get_db()


@router.get("s", status_code=200)
async def get_all_reservations():
    result = db.query(reservationModel).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "hotel_id": r.hotel_id,
            "room_id": r.room_id,
            "user_id": r.user_id,
            "number_occupants": r.number_occupants,
            "start_date": r.start_date.isoformat(),
            "end_date": r.end_date.isoformat(),
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("/{reservation_id}", status_code=200)
async def get_reservation(reservation_id: int):
    result = (
        db.query(reservationModel).filter(reservationModel.id == reservation_id).first()
    )

    if result is None:
        raise HTTPException(status_code=404)

    json_return = {
        "id": result.id,
        "hotel_id": result.hotel_id,
        "room_id": result.room_id,
        "user_id": result.user_id,
        "number_occupants": result.number_occupants,
        "start_date": result.start_date.isoformat(),
        "end_date": result.end_date.isoformat(),
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.post("", status_code=201)
async def add_reservation(
    reservationRequestDto: reservationRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(reservationRequestDto)
    reservation: reservationModel | None = (
        db.query(reservationModel)
        .filter(
            reservationModel.hotel_id == reservationRequestDto.hotel_id
            and reservationModel.room_id == reservationRequestDto.room_id
            and (
                reservationModel.start_date.between(
                    reservationRequestDto.start_date, reservationRequestDto.end_date
                )
                or reservationModel.end_date.between(
                    reservationRequestDto.start_date, reservationRequestDto.end_date
                )
                or (
                    reservationModel.start_date <= reservationRequestDto.start_date
                    and reservationModel.end_date >= reservationRequestDto.end_date
                )
            )
        )
        .first()
    )
    if reservation is not None:
        raise HTTPException(status_code=409)
    result: reservationModel = reservationModel(
        hotel_id=reservationRequestDto.hotel_id,
        room_id=reservationRequestDto.room_id,
        user_id=reservationRequestDto.user_id,
        number_occupants=reservationRequestDto.number_occupants,
        start_date=reservationRequestDto.start_date,
        end_date=reservationRequestDto.end_date,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    if result is None:
        raise HTTPException(status_code=500)
    db.add(result)
    db.commit()
    json_return = {
        "id": result.id,
        "hotel_id": result.hotel_id,
        "room_id": result.room_id,
        "user_id": result.user_id,
        "number_occupants": result.number_occupants,
        "start_date": result.start_date.isoformat(),
        "end_date": result.end_date.isoformat(),
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.put("/{reservation_id}", status_code=200)
async def update_reservation(
    reservation_id: int,
    reservationRequestDto: reservationRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(reservationRequestDto)

    try:
        db.query(reservationModel).filter(reservationModel.id == reservation_id).update(
            {
                reservationModel.hotel_id: reservationRequestDto.hotel_id,
                reservationModel.room_id: reservationRequestDto.room_id,
                reservationModel.user_id: reservationRequestDto.user_id,
                reservationModel.number_occupants: reservationRequestDto.number_occupants,
                reservationModel.start_date: reservationRequestDto.start_date,
                reservationModel.end_date: reservationRequestDto.end_date,
                reservationModel.updated_at: datetime.now(),
            }
        )
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code=404)

    return "UPDATED"


@router.delete("/{reservation_id}", status_code=200)
async def delete_reservation(
    reservation_id: int, authorized: bool = Depends(verify_token)
):
    result = db.get(reservationModel, reservation_id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
