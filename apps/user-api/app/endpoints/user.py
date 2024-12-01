from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.routes import router
from app.models.user import userModel
from app.dtos.userDtos import userRequestDto

import app.sql_engine as database

from sqlalchemy.exc import IntegrityError

import logging

import os

import jwt
import bcrypt

from app.utils.tokenUtils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    JWT_SECRET_KEY,
    verify_token,
)


router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


db = database.get_db()


@router.get("s", status_code=200)
async def get_all_users():
    result = db.query(userModel).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "mail": r.mail,
            "password": r.password,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("/{user_id}", status_code=200)
async def get_user(user_id: int):
    result = db.query(userModel).filter(userModel.id == user_id).first()

    if result is None:
        raise HTTPException(status_code=404)

    json_return = {
        "id": result.id,
        "mail": result.mail,
        "password": result.password,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.post("/create-token", status_code=201)
async def create_token(userRequestDto: userRequestDto):
    logging.error(userRequestDto.password)
    user: userModel | None = (
        db.query(userModel).filter(userModel.mail == userRequestDto.mail).first()
    )
    logging.error(user)
    if user is None:
        raise HTTPException(status_code=404)
    if user.password != userRequestDto.password:
        raise HTTPException(status_code=403)
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_dict = {"exp": expire_time, "sub": userRequestDto.mail}
    logging.error(access_token_dict)
    return {"access_token": jwt.encode(access_token_dict, JWT_SECRET_KEY, ALGORITHM)}


@router.post("", status_code=201)
async def add_user(userRequestDto: userRequestDto):
    logging.error(userRequestDto)
    user: userModel | None = (
        db.query(userModel).filter(userModel.mail == userRequestDto.mail).first()
    )
    if user is not None:
        raise HTTPException(status_code=409)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(userRequestDto.password.encode("utf-8"), salt)
    result: userModel = userModel(
        mail=userRequestDto.mail,
        password=hashed,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    if bcrypt.checkpw(
        userRequestDto.password.encode("utf-8"),
        hashed,
    ):
        print("match")
    else:
        print("does not match")
    if result is None:
        raise HTTPException(status_code=500)
    db.add(result)
    db.commit()
    json_return = {
        "id": result.id,
        "mail": result.mail,
        "password": result.password,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.put("/{user_id}", status_code=200)
async def update_user(
    user_id: int,
    userRequestDto: userRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(userRequestDto)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(userRequestDto.password.encode("utf-8"), salt)

    try:
        db.query(userModel).filter(userModel.id == user_id).update(
            {
                userModel.mail: userRequestDto.mail,
                userModel.password: hashed,
                userModel.updated_at: datetime.now(),
            }
        )
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=404)

    return "UPDATED"


@router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: int, authorized: bool = Depends(verify_token)):
    result = db.get(userModel, user_id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
