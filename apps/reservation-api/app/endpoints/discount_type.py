from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.routes import router
from app.models.discount_type import discountTypeModel
from app.dtos.discountTypeDtos import discountTypeRequestDto

import app.sql_engine as database

from sqlalchemy.exc import IntegrityError

import logging

import os

import jwt
import bcrypt

from app.utils.tokenUtils import verify_token

router = APIRouter(
    prefix="/discount-type",
    tags=["DiscountType"],
    responses={404: {"description": "Not found"}},
)

"""
Routes pour Reservation
"""

db = database.get_db()


@router.get("s", status_code=200)
async def get_all_discount_types():
    result = db.query(discountTypeModel).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "name": r.name,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("/{discount_type_id}", status_code=200)
async def get_discount_type(discount_type_id: int):
    result = (
        db.query(discountTypeModel)
        .filter(discountTypeModel.id == discount_type_id)
        .first()
    )

    if result is None:
        raise HTTPException(status_code=404)

    json_return = {
        "id": result.id,
        "name": result.name,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.post("", status_code=201)
async def add_discount_type(
    discountTypeRequestDto: discountTypeRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(discountTypeRequestDto)
    discount_type: discountTypeModel | None = (
        db.query(discountTypeModel)
        .filter(discountTypeModel.name == discountTypeRequestDto.name)
        .first()
    )
    if discount_type is not None:
        raise HTTPException(status_code=409)
    result: discountTypeModel = discountTypeModel(
        name=discountTypeRequestDto.name,
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
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.put("/{discount_type_id}", status_code=200)
async def update_discount_type(
    discount_type_id: int,
    discountTypeRequestDto: discountTypeRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(discountTypeRequestDto)

    try:
        db.query(discountTypeModel).filter(
            discountTypeModel.id == discount_type_id
        ).update(
            {
                discountTypeModel.name: discountTypeRequestDto.name,
                discountTypeModel.updated_at: datetime.now(),
            }
        )
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code=404)

    return "UPDATED"


@router.delete("/{discount_type_id}", status_code=200)
async def delete_discount_type(
    discount_type_id: int, authorized: bool = Depends(verify_token)
):
    result = db.get(discountTypeModel, discount_type_id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
