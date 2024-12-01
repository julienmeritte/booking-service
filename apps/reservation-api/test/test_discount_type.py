from fastapi.testclient import TestClient
import jwt
import pytest

import logging, os
from datetime import datetime, timedelta
import app.sql_engine as database

from app.models.reservation import reservationModel
from app.models.reservation_additional_service import reservationServiceModel
from app.models.discount import discountModel
from app.models.discount_type import discountTypeModel
from app.models.hotel import hotelModel
from app.models.hotel_room import roomModel
from app.models.user import userModel
from app.models.room_category import roomCategoryModel
from app.models.additional_service import serviceModel

from main import app

client = TestClient(app)

db = database.get_db()

discountTypeMock = {}
headers = {}


@pytest.fixture(scope="session", autouse=True)
def db_setup():
    # Will be executed before the first test
    db.query(discountModel).delete()
    db.commit()
    db.query(discountTypeModel).delete()
    db.commit()
    db.query(reservationServiceModel).delete()
    db.commit()
    db.query(reservationModel).delete()
    db.commit()
    db.query(userModel).delete()
    db.commit()
    db.query(roomModel).delete()
    db.commit()
    db.query(serviceModel).delete()
    db.commit()
    db.query(roomCategoryModel).delete()
    db.commit()
    db.query(hotelModel).delete()
    db.commit()

    result: userModel = userModel(
        id=1,
        mail="testjulien@gmail.com",
        password="testoui".encode("utf-8"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(result)
    db.commit()

    global headers
    access_token_dict = {
        "exp": datetime.utcnow() + timedelta(minutes=1200),
        "sub": "testjulien@gmail.com",
    }
    token = jwt.encode(access_token_dict, os.environ["JWT_SECRET_KEY"], "HS256")
    headers = {"Authorization": "Bearer " + token}

    yield 1
    # Will be executed after the last test
    db.rollback()


def test_add_discount_type_success(db_setup):
    """Test function for POST /discount-type 201 CREATED"""

    global discountTypeMock
    global headers
    response = client.post(
        "/discount-type",
        json={
            "name": "DISCOUNT_TUESDAY",
        },
        headers=headers,
    )
    assert response.status_code == 201, response.text
    discountTypeMock = response.json()


def test_add_discount_type_conflict(db_setup):
    """Test function for POST /discount-type 409 CONFLICT"""

    global headers
    response = client.post(
        "/discount-type",
        json={
            "name": "DISCOUNT_TUESDAY",
        },
        headers=headers,
    )
    assert response.status_code == 409, response.text


def test_add_discount_type_unauthorized(db_setup):
    """Test function for POST /discount-type 401 UNAUTHORIZED"""

    global discountTypeMock
    global headers
    response = client.post(
        "/discount-type",
        json={
            "name": "DISCOUNT_TUESDAY",
        },
    )
    assert response.status_code == 401, response.text


def test_get_discount_type_success(db_setup):
    """Test function for GET /discount-type 200 OK"""

    response = client.get("/discount-types")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "DISCOUNT_TUESDAY"


def test_get_discount_type_id_success(db_setup):
    """Test function for GET /discount-type/{id} 200 OK"""

    global discountTypeMock
    response = client.get("/discount-type/" + str(discountTypeMock["id"]))
    assert response.status_code == 200, response.text


def test_update_discount_type_unauthorized(db_setup):
    """Test function for PUT /discount-type/{id} 401 UNAUTHORIZED"""
    global discountTypeMock
    response = client.put(
        "/discount-type/" + str(discountTypeMock["id"]),
        json={
            "name": "DISCOUNT_TUESDAY",
        },
    )
    assert response.status_code == 401


def test_update_discount_type_success(db_setup):
    """Test function for PUT /discount-type/{id} 200 OK"""
    global discountTypeMock
    global headers
    response = client.put(
        "/discount-type/" + str(discountTypeMock["id"]),
        json={
            "name": "DISCOUNT_TUESDAY",
        },
        headers=headers,
    )
    assert response.status_code == 200


def test_delete_discount_type_unauthorized(db_setup):
    """Test function for DELETE /discount-type/{id} 401 UNAUTHORIZED"""
    global discountTypeMock
    response = client.delete(
        "/discount-type/" + str(discountTypeMock["id"]),
    )
    assert response.status_code == 401


def test_delete_discount_type_success(db_setup):
    """Test function for DELETE /discount-type/{id} 200 OK"""
    global discountTypeMock
    global headers
    response = client.delete(
        "/discount-type/" + str(discountTypeMock["id"]),
        headers=headers,
    )
    assert response.status_code == 200
