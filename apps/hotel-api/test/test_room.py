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

roomMock = {}
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

    result: roomCategoryModel = roomCategoryModel(
        id=1,
        name="Chambre d'hôte",
        max_occupancy=3,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(result)
    db.commit()

    result: hotelModel = hotelModel(
        id=1,
        name="Hôtel de la croisée",
        address="1 rue des cheminées",
        phone_number="0111111111",
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


def test_add_room_success(db_setup):
    """Test function for POST /room 201 CREATED"""

    global roomMock
    global headers
    response = client.post(
        "/room",
        json={
            "hotel_id": 1,
            "room_number": "AB200",
            "category_id": 1,
        },
        headers=headers,
    )
    assert response.status_code == 201, response.text
    roomMock = response.json()


def test_add_room_unauthorized(db_setup):
    """Test function for POST /room 401 UNAUTHORIZED"""

    global roomMock
    global headers
    response = client.post(
        "/room",
        json={
            "hotel_id": 1,
            "room_number": "AB200",
            "category_id": 1,
        },
    )
    assert response.status_code == 401, response.text


def test_get_room_success(db_setup):
    """Test function for GET /rooms 200 OK"""

    response = client.get("/rooms")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["hotel_id"] == 1
    assert response.json()[0]["category_id"] == 1


def test_get_room_id_success(db_setup):
    """Test function for GET /room/{id} 200 OK"""

    global roomMock
    logging.warning(roomMock)
    response = client.get("/room/" + str(roomMock["id"]))
    assert response.status_code == 200, response.text


def test_update_room_unauthorized(db_setup):
    """Test function for PUT /room/{id} 401 UNAUTHORIZED"""
    global roomMock
    response = client.put(
        "/room/" + str(roomMock["id"]),
        json={
            "hotel_id": 1,
            "room_number": "AB200",
            "category_id": 1,
        },
    )
    assert response.status_code == 401


def test_update_room_success(db_setup):
    """Test function for PUT /room/{id} 200 OK"""
    global roomMock
    global headers
    response = client.put(
        "/room/" + str(roomMock["id"]),
        json={
            "hotel_id": 1,
            "room_number": "AB200",
            "category_id": 1,
        },
        headers=headers,
    )
    assert response.status_code == 200


def test_delete_room_unauthorized(db_setup):
    """Test function for DELETE /room/{id} 401 UNAUTHORIZED"""
    global roomMock
    response = client.delete(
        "/room/" + str(roomMock["id"]),
    )
    assert response.status_code == 401


def test_delete_room_success(db_setup):
    """Test function for DELETE /room/{id} 200 OK"""
    global roomMock
    global headers
    response = client.delete(
        "/room/" + str(roomMock["id"]),
        headers=headers,
    )
    assert response.status_code == 200
