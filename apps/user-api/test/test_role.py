from fastapi.testclient import TestClient
import jwt
import pytest

import logging, os
from datetime import datetime, timedelta
import app.sql_engine as database
from app.models.user import userModel
from app.models.role import roleModel, roleUserModel

from main import app

client = TestClient(app)

db = database.get_db()

roleMock = {}
headers = {}


@pytest.fixture(scope="session", autouse=True)
def db_setup():
    # Will be executed before the first test
    db.query(roleUserModel).delete()
    db.query(userModel).delete()
    db.query(roleModel).delete()
    db.commit()
    result: userModel = userModel(
        mail="julien@gmail.com",
        password="ouinon".encode("utf-8"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(result)
    db.commit()
    global headers
    access_token_dict = {
        "exp": datetime.utcnow() + timedelta(minutes=1200),
        "sub": "julien@gmail.com",
    }
    token = jwt.encode(access_token_dict, os.environ["JWT_SECRET_KEY"], "HS256")
    headers = {"Authorization": "Bearer " + token}
    yield 1
    # Will be executed after the last test
    db.rollback()


def test_add_role_success(db_setup):
    """Test function for POST /role 201 CREATED"""

    global roleMock
    global headers
    response = client.post("/role", json={"name": "admin"}, headers=headers)
    assert response.status_code == 201, response.text
    roleMock = response.json()


def test_add_role_conflict(db_setup):
    """Test function for POST /role 409 CONFLICT"""

    response = client.post("/role", json={"name": "admin"}, headers=headers)

    assert response.status_code == 409, response.text


def test_add_role_unauthorized(db_setup):
    """Test function for POST /role 401 UNAUTHORIZED"""

    response = client.post("/role", json={"name": "admin"})

    assert response.status_code == 401, response.text


def test_get_roles_success(db_setup):
    """Test function for GET /roles 200 OK"""

    response = client.get("/roles")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "admin"


def test_get_role_id_success(db_setup):
    """Test function for GET /role/{id} 200 OK"""

    global roleMock
    logging.warning(roleMock)
    response = client.get("/role/" + str(roleMock["id"]))
    assert response.status_code == 200, response.text


def test_update_role_unauthorized(db_setup):
    """Test function for PUT /role/{id} 401 UNAUTHORIZED"""
    global roleMock
    response = client.put(
        "/role/" + str(roleMock["id"]),
        json={"name": roleMock["name"]},
    )
    assert response.status_code == 401


def test_update_role_success(db_setup):
    """Test function for PUT /role/{id} 200 OK"""
    global roleMock
    global headers
    response = client.put(
        "/role/" + str(roleMock["id"]),
        json={"name": roleMock["name"]},
        headers=headers,
    )
    assert response.status_code == 200


def test_delete_role_unauthorized(db_setup):
    """Test function for DELETE /role/{id} 401 UNAUTHORIZED"""
    global roleMock
    response = client.delete(
        "/role/" + str(roleMock["id"]),
    )
    assert response.status_code == 401


def test_delete_role_success(db_setup):
    """Test function for DELETE /role/{id} 200 OK"""
    global roleMock
    global headers
    response = client.delete(
        "/role/" + str(roleMock["id"]),
        headers=headers,
    )
    assert response.status_code == 200
