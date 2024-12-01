from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.routes import router
from app.models.reservation_additional_service import reservationServiceModel
from app.dtos.reservationServiceDtos import reservationServiceRequestDto

import app.sql_engine as database

from sqlalchemy.exc import IntegrityError

import logging

import os

import jwt
import bcrypt

from app.utils.tokenUtils import verify_token

router = APIRouter(
    prefix="/reservation-service",
    tags=["ReservationService"],
    responses={404: {"description": "Not found"}},
)

"""
Routes pour Reservation
"""

db = database.get_db()


@router.get("s", status_code=200)
async def get_all_reservations_service():
    result = db.query(reservationServiceModel).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "reservation_id": r.reservation_id,
            "additional_service_id": r.additional_service_id,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("/{reservation_service_id}", status_code=200)
async def get_reservation_service(reservation_service_id: int):
    result = (
        db.query(reservationServiceModel)
        .filter(reservationServiceModel.id == reservation_service_id)
        .first()
    )

    if result is None:
        raise HTTPException(status_code=404)

    json_return = {
        "id": result.id,
        "reservation_id": result.reservation_id,
        "additional_service_id": result.additional_service_id,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.post("", status_code=201)
async def add_reservation_service(
    reservationServiceRequestDto: reservationServiceRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(reservationServiceRequestDto)
    reservation_service: reservationServiceModel | None = (
        db.query(reservationServiceModel)
        .filter(
            reservationServiceModel.reservation_id
            == reservationServiceRequestDto.reservation_id
            and reservationServiceModel.additional_service_id
            == reservationServiceRequestDto.additional_service_id
        )
        .first()
    )
    if reservation_service is not None:
        raise HTTPException(status_code=409)
    result: reservationServiceModel = reservationServiceModel(
        reservation_id=reservationServiceRequestDto.reservation_id,
        additional_service_id=reservationServiceRequestDto.additional_service_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    if result is None:
        raise HTTPException(status_code=500)
    db.add(result)
    db.commit()
    json_return = {
        "id": result.id,
        "reservation_id": result.reservation_id,
        "additional_service_id": result.additional_service_id,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.put("/{reservation_service_id}", status_code=200)
async def update_reservation_service(
    reservation_service_id: int,
    reservationServiceRequestDto: reservationServiceRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(reservationServiceRequestDto)

    try:
        db.query(reservationServiceModel).filter(
            reservationServiceModel.id == reservation_service_id
        ).update(
            {
                reservationServiceModel.reservation_id: reservationServiceRequestDto.reservation_id,
                reservationServiceModel.additional_service_id: reservationServiceRequestDto.additional_service_id,
                reservationServiceModel.updated_at: datetime.now(),
            }
        )
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code=404)

    return "UPDATED"


@router.delete("/{reservation_service_id}", status_code=200)
async def delete_reservation_service(
    reservation_service_id: int, authorized: bool = Depends(verify_token)
):
    result = db.get(reservationServiceModel, reservation_service_id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
