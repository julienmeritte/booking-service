from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.routes import router

import logging
from datetime import datetime

import app.sql_engine as database

from app.models.additional_service import serviceModel

from app.dtos.serviceDtos import serviceRequestDto

from app.utils.tokenUtils import verify_token

router = APIRouter(
    prefix="/service",
    tags=["Services"],
    responses={404: {"description": "Not found"}},
)

db = database.get_db()


"""
CRUD Services
"""


@router.get("s", status_code=200)
async def get_all_services():
    result = db.query(serviceModel).all()
    json_return = []
    for r in result:
        object = {
            "id": r.id,
            "name": r.name,
            "max_number": r.max_number,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        json_return.append(object)
    return JSONResponse(content=json_return)


@router.get("/{service_id}", status_code=200)
async def get_service(service_id: int):
    result = db.query(serviceModel).filter(serviceModel.id == service_id).first()
    if result is None:
        raise HTTPException(status_code=404)
    json_return = {
        "id": result.id,
        "name": result.name,
        "max_occupancy": result.max_number,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.post("", status_code=201)
async def add_service(
    serviceRequestDto: serviceRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(serviceRequestDto)
    result: serviceModel = serviceModel(
        name=serviceRequestDto.name,
        max_number=serviceRequestDto.max_number,
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
        "max_number": result.max_number,
        "created_at": result.created_at.isoformat(),
        "updated_at": result.updated_at.isoformat(),
    }
    return json_return


@router.put("/{service_id}", status_code=200)
async def update_service(
    service_id: int,
    serviceRequestDto: serviceRequestDto,
    authorized: bool = Depends(verify_token),
):
    logging.error(serviceRequestDto)
    db.query(serviceModel).filter(serviceModel.id == service_id).update(
        {
            serviceModel.name: serviceRequestDto.name,
            serviceModel.max_number: serviceRequestDto.max_number,
            serviceModel.updated_at: datetime.now(),
        }
    )
    db.commit()
    return "UPDATED"


@router.delete("/{service_id}", status_code=200)
async def delete_service(service_id: int, authorized: bool = Depends(verify_token)):
    result = db.get(serviceModel, service_id)
    if result is None:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return "DELETED"
