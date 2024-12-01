from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.routes import router
from app.models.role import roleModel, roleUserModel
from app.dtos.roleDtos import roleUserRequestDto

import app.sql_engine as database

from sqlalchemy.exc import IntegrityError

import logging

from app.utils.tokenUtils import verify_token


router = APIRouter(
    prefix="/role-users",
    tags=["RoleUsers"],
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
Routes pour Role liés au User
"""


@router.get("", status_code=200)
async def get_all_user_by_roles():
    result = db.query(roleUserModel).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "role_id": r.role_id,
            "user_id": r.user_id,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("/{role_user_id}", status_code=200)
async def get_user_role(role_user_id: int):
    result = db.query(roleUserModel).filter(roleUserModel.id == role_user_id).first()

    if result is None:
        raise HTTPException(status_code=404)

    json_return = {
        "id": result.id,
        "role_id": result.role_id,
        "user_id": result.user_id,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.post("", status_code=201)
async def add_user_role(
    roleUserRequestDto: roleUserRequestDto, authorized: bool = Depends(verify_token)
):
    logging.error(roleUserRequestDto)
    userRole: roleUserModel | None = (
        db.query(roleUserModel)
        .filter(
            roleUserModel.role_id == roleUserRequestDto.role_id
            and roleUserModel.user_id == roleUserRequestDto.user_id
        )
        .first()
    )
    if userRole is not None:
        raise HTTPException(status_code=409)
    result: roleUserModel = roleUserModel(
        role_id=roleUserRequestDto.role_id,
        user_id=roleUserRequestDto.user_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    if result is None:
        raise HTTPException(status_code=500)
    db.add(result)
    db.commit()
    json_return = {
        "id": result.id,
        "user_id": result.user_id,
        "role_id": result.role_id,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.put("/{user_role_id}", status_code=200)
async def update_role(
    user_role_id: int,
    roleUserRequestDto: roleUserRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(roleUserRequestDto)

    try:
        db.query(roleUserModel).filter(roleUserModel.id == user_role_id).update(
            {
                roleUserModel.role_id: roleUserRequestDto.role_id,
                roleUserModel.user_id: roleUserRequestDto.user_id,
                roleUserModel.updated_at: datetime.now(),
            }
        )
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code=404)

    return "UPDATED"


@router.delete("/{user_role_id}", status_code=200)
async def delete_role(user_role_id: int, authorized: bool = Depends(verify_token)):
    result = db.get(roleUserModel, user_role_id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
