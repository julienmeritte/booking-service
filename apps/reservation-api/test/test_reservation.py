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

reservationMock = {}
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

    result: hotelModel = hotelModel(
        id=1,
        name="Hotel du test",
        address="1 Avenue du Test",
        phone_number="0111111111",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(result)
    db.commit()

    result: roomCategoryModel = roomCategoryModel(
        id=1,
        name="Chambre de luxe",
        max_occupancy=3,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(result)
    db.commit()

    result: roomModel = roomModel(
        id=1,
        hotel_id=1,
        room_number="1000",
        category_id=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(result)
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


def test_add_reservation_success(db_setup):
    """Test function for POST /reservation 201 CREATED"""

    global reservationMock
    global headers
    response = client.post(
        "/reservation",
        json={
            "hotel_id": 1,
            "room_id": 1,
            "user_id": 1,
            "number_occupants": 3,
            "start_date": datetime.now().isoformat(),
            "end_date": datetime.now().isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 201, response.text
    reservationMock = response.json()


def test_add_reservation_conflict(db_setup):
    """Test function for POST /reservation 409 CONFLICT"""

    global headers
    response = client.post(
        "/reservation",
        json={
            "hotel_id": 1,
            "room_id": 1,
            "user_id": 1,
            "number_occupants": 3,
            "start_date": datetime.now().isoformat(),
            "end_date": datetime.now().isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 409, response.text


def test_add_reservation_unauthorized(db_setup):
    """Test function for POST /reservation 401 UNAUTHORIZED"""

    global reservationMock
    global headers
    response = client.post(
        "/reservation",
        json={
            "hotel_id": 1,
            "room_id": 1,
            "user_id": 1,
            "number_occupants": 3,
            "start_date": datetime.now().isoformat(),
            "end_date": datetime.now().isoformat(),
        },
    )
    assert response.status_code == 401, response.text


def test_get_reservations_success(db_setup):
    """Test function for GET /reservations 200 OK"""

    response = client.get("/reservations")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["room_id"] == 1
    assert response.json()[0]["user_id"] == 1
    assert response.json()[0]["hotel_id"] == 1


def test_get_reservation_id_success(db_setup):
    """Test function for GET /reservation/{id} 200 OK"""

    global reservationMock
    response = client.get("/reservation/" + str(reservationMock["id"]))
    assert response.status_code == 200, response.text


def test_update_reservation_unauthorized(db_setup):
    """Test function for PUT /reservation/{id} 401 UNAUTHORIZED"""
    global reservationMock
    response = client.put(
        "/reservation/" + str(reservationMock["id"]),
        json={
            "hotel_id": 1,
            "room_id": 1,
            "user_id": 1,
            "number_occupants": 3,
            "start_date": datetime.now().isoformat(),
            "end_date": datetime.now().isoformat(),
        },
    )
    assert response.status_code == 401


def test_update_reservation_success(db_setup):
    """Test function for PUT /reservation/{id} 200 OK"""
    global reservationMock
    global headers
    response = client.put(
        "/reservation/" + str(reservationMock["id"]),
        json={
            "hotel_id": 1,
            "room_id": 1,
            "user_id": 1,
            "number_occupants": 3,
            "start_date": datetime.now().isoformat(),
            "end_date": datetime.now().isoformat(),
        },
        headers=headers,
    )
    assert response.status_code == 200


def test_delete_reservation_unauthorized(db_setup):
    """Test function for DELETE /reservation/{id} 401 UNAUTHORIZED"""
    global reservationMock
    response = client.delete(
        "/reservation/" + str(reservationMock["id"]),
    )
    assert response.status_code == 401


def test_delete_reservation_success(db_setup):
    """Test function for DELETE /reservation/{id} 200 OK"""
    global reservationMock
    global headers
    response = client.delete(
        "/reservation/" + str(reservationMock["id"]),
        headers=headers,
    )
    assert response.status_code == 200
