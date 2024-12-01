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

roleUserMock = {}
headers = {}


@pytest.fixture(scope="session", autouse=True)
def db_setup():
    # Will be executed before the first test
    db.query(roleUserModel).delete()
    db.commit()
    db.query(userModel).delete()
    db.commit()
    db.query(roleModel).delete()
    db.commit()

    result: userModel = userModel(
        id="1",
        mail="testjulien@gmail.com",
        password="testoui".encode("utf-8"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(result)
    db.commit()

    result: roleModel = roleModel(
        id="1",
        name="admin",
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


def test_add_user_role_success(db_setup):
    """Test function for POST /role-users 201 CREATED"""

    global roleUserMock
    global headers
    response = client.post(
        "/role-users",
        json={"role_id": 1, "user_id": 1},
        headers=headers,
    )
    assert response.status_code == 201, response.text
    roleUserMock = response.json()


def test_add_user_role_conflict(db_setup):
    """Test function for POST /role-users 409 CONFLICT"""

    global roleUserMock
    global headers
    response = client.post(
        "/role-users", json={"role_id": 1, "user_id": 1}, headers=headers
    )
    assert response.status_code == 409, response.text


def test_add_user_role_unauthorized(db_setup):
    """Test function for POST /role-users 401 UNAUTHORIZED"""

    global roleUserMock
    global headers
    response = client.post(
        "/role-users",
        json={"role_id": 1, "user_id": 1},
    )
    assert response.status_code == 401, response.text


def test_get_user_roles_success(db_setup):
    """Test function for GET /role-users 200 OK"""

    response = client.get("/role-users")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["role_id"] == 1
    assert response.json()[0]["user_id"] == 1


def test_get_user_role_id_success(db_setup):
    """Test function for GET /role-users/{id} 200 OK"""

    global roleUserMock
    logging.warning(roleUserMock)
    response = client.get("/role-users/" + str(roleUserMock["id"]))
    assert response.status_code == 200, response.text


def test_update_user_role_unauthorized(db_setup):
    """Test function for PUT /role-users/{id} 401 UNAUTHORIZED"""
    global roleUserMock
    response = client.put(
        "/role-users/" + str(roleUserMock["id"]),
        json={"role_id": 1, "user_id": 1},
    )
    assert response.status_code == 401


def test_update_user_role_success(db_setup):
    """Test function for PUT /role-users/{id} 200 OK"""
    global roleUserMock
    global headers
    response = client.put(
        "/role-users/" + str(roleUserMock["id"]),
        json={"role_id": 1, "user_id": 1},
        headers=headers,
    )
    assert response.status_code == 200


def test_delete_user_role_unauthorized(db_setup):
    """Test function for DELETE /role-users/{id} 401 UNAUTHORIZED"""
    global roleUserMock
    response = client.delete(
        "/role-users/" + str(roleUserMock["id"]),
    )
    assert response.status_code == 401


def test_delete_user_role_success(db_setup):
    """Test function for DELETE /role-users/{id} 200 OK"""
    global roleUserMock
    global headers
    response = client.delete(
        "/role-users/" + str(roleUserMock["id"]),
        headers=headers,
    )
    assert response.status_code == 200
