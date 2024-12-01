from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.routes import router
from app.models.discount import discountModel
from app.dtos.discountDtos import discountRequestDto

import app.sql_engine as database

from sqlalchemy.exc import IntegrityError

import logging

import os

import jwt
import bcrypt

from app.utils.tokenUtils import verify_token

router = APIRouter(
    prefix="/discount",
    tags=["Discount"],
    responses={404: {"description": "Not found"}},
)

"""
Routes pour Reservation
"""

db = database.get_db()


@router.get("s", status_code=200)
async def get_all_discounts():
    result = db.query(discountModel).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "discount_type_id": r.discount_type_id,
            "start_date": r.start_date.isoformat(),
            "end_date": r.end_date.isoformat(),
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("/{discount_id}", status_code=200)
async def get_discount(discount_id: int):
    result = db.query(discountModel).filter(discountModel.id == discount_id).first()

    if result is None:
        raise HTTPException(status_code=404)

    json_return = {
        "id": result.id,
        "discount_type_id": result.discount_type_id,
        "start_date": result.start_date.isoformat(),
        "end_date": result.end_date.isoformat(),
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.post("", status_code=201)
async def add_discount(
    discountRequestDto: discountRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(discountRequestDto)
    discount: discountModel | None = (
        db.query(discountModel)
        .filter(discountModel.discount_type_id == discountRequestDto.discount_type_id)
        .first()
    )
    if discount is not None:
        raise HTTPException(status_code=409)

    result: discountModel = discountModel(
        discount_type_id=discountRequestDto.discount_type_id,
        start_date=discountRequestDto.start_date,
        end_date=discountRequestDto.end_date,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    if result is None:
        raise HTTPException(status_code=500)
    db.add(result)
    db.commit()
    json_return = {
        "id": result.id,
        "discount_type_id": result.discount_type_id,
        "start_date": result.start_date.isoformat(),
        "end_date": result.end_date.isoformat(),
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.put("/{discount_id}", status_code=200)
async def update_discount(
    discount_id: int,
    discountRequestDto: discountRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(discountRequestDto)

    try:
        db.query(discountModel).filter(discountModel.id == discount_id).update(
            {
                discountModel.discount_type_id: discountRequestDto.discount_type_id,
                discountModel.start_date: discountRequestDto.start_date,
                discountModel.end_date: discountRequestDto.end_date,
                discountModel.updated_at: datetime.now(),
            }
        )
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code=404)

    return "UPDATED"


@router.delete("/{discount_id}", status_code=200)
async def delete_discount(discount_id: int, authorized: bool = Depends(verify_token)):
    result = db.get(discountModel, discount_id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
