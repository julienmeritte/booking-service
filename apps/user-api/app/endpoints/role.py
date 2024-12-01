from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.routes import router
from app.models.role import roleModel, roleModel
from app.dtos.userDtos import userRequestDto
from app.dtos.roleDtos import roleRequestDto, roleUserRequestDto

import app.sql_engine as database

from sqlalchemy.exc import IntegrityError

import logging

import os

import jwt
import bcrypt

from app.utils.tokenUtils import verify_token


router = APIRouter(
    prefix="/role",
    tags=["Role"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    try:
        db = database.SessionLocal()
        logging.info(" [SQL] : Connect to DB Ok")
        return db
    except:
        logging.info(" [SQL] : Connect to DB Failed")
        db.close()


db = get_db()


"""
Routes pour Roles
"""


@router.get("s", status_code=200)
async def get_all_roles():
    result = db.query(roleModel).all()
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


@router.get("/{role_id}", status_code=200)
async def get_role(role_id: int):
    result = db.query(roleModel).filter(roleModel.id == role_id).first()

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
async def add_role(
    roleRequestDto: roleRequestDto, authorized: bool = Depends(verify_token)
):
    logging.error(roleRequestDto)
    role: roleModel | None = (
        db.query(roleModel).filter(roleModel.name == roleRequestDto.name).first()
    )
    if role is not None:
        raise HTTPException(status_code=409)
    result: roleModel = roleModel(
        name=roleRequestDto.name,
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


@router.put("/{role_id}", status_code=200)
async def update_role(
    role_id: int,
    roleRequestDto: roleRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(roleRequestDto)

    try:
        db.query(roleModel).filter(roleModel.id == role_id).update(
            {
                roleModel.name: roleRequestDto.name,
                roleModel.updated_at: datetime.now(),
            }
        )
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code=404)

    return "UPDATED"


@router.delete("/{role_id}", status_code=200)
async def delete_role(role_id: int, authorized: bool = Depends(verify_token)):
    result = db.get(roleModel, role_id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
