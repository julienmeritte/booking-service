from fastapi.testclient import TestClient
import pytest

import logging, os
import app.sql_engine as database
from app.models.user import userModel
from app.models.role import roleModel, roleUserModel

from main import app

client = TestClient(app)

db = database.get_db()

julienMock = {}
token = ""


@pytest.fixture(scope="session", autouse=True)
def db_setup():
    # Will be executed before the first test
    db.query(roleUserModel).delete()
    db.commit()
    db.query(userModel).delete()
    db.commit()
    db.query(roleModel).delete()
    db.commit()
    yield 1
    # Will be executed after the last test
    db.rollback()


def test_add_user_success(db_setup):
    """Test function for POST /user 201 CREATED"""

    global julienMock
    response = client.post(
        "/user", json={"mail": "testjulien@gmail.com", "password": "testoui"}
    )
    assert response.status_code == 201, response.text
    julienMock = response.json()
    logging.debug("\nLogging julienMock ---> {0}".format(julienMock))


def test_add_user_conflict(db_setup):
    """Test function for POST /user 409 CONFLICT"""

    global julienMock
    response = client.post(
        "/user", json={"mail": "testjulien@gmail.com", "password": "testoui"}
    )
    assert response.status_code == 409, response.text
    logging.debug("\nLogging julienMock ---> {0}".format(response.json()))


def test_get_users_success(db_setup):
    """Test function for GET /users 200 OK"""

    response = client.get("/users")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["mail"] == "testjulien@gmail.com"


def test_get_user_id_success(db_setup):
    """Test function for GET /user/{id} 200 OK"""

    global julienMock
    logging.warning(julienMock)
    response = client.get("/user/" + str(julienMock["id"]))
    assert response.status_code == 200, response.text


def test_create_token_success(db_setup):
    """Test function for POST /user/create-token 201 CREATED"""
    global julienMock
    global token
    response = client.post(
        "/user/create-token",
        json={"mail": julienMock["mail"], "password": julienMock["password"]},
    )
    assert response.status_code == 201, response.text
    token = response.json()


def test_create_token_not_found(db_setup):
    """Test function for POST /user/create-token 404 NOT FOUND"""
    global julienMock
    response = client.post(
        "/user/create-token",
        json={"mail": "stranger@gmail.com", "password": julienMock["password"]},
    )
    assert response.status_code == 404, response.text


def test_create_token_forbidden(db_setup):
    """Test function for POST /user/create-token 403 FORBIDDEN"""
    global julienMock
    response = client.post(
        "/user/create-token",
        json={"mail": julienMock["mail"], "password": julienMock["password"] + "bad"},
    )
    assert response.status_code == 403, response.text


def test_update_user_unauthorized(db_setup):
    """Test function for PUT /user/{id} 401 UNAUTHORIZED"""
    global julienMock
    response = client.put(
        "/user/" + str(julienMock["id"]),
        json={"mail": julienMock["mail"], "password": "testnon"},
    )
    assert response.status_code == 401


def test_update_user_success(db_setup):
    """Test function for PUT /user/{id} 200 OK"""
    global julienMock
    global token
    headers = {"Authorization": "Bearer {}".format(token["access_token"])}
    response = client.put(
        "/user/" + str(julienMock["id"]),
        json={"mail": julienMock["mail"], "password": "testnon"},
        headers=headers,
    )
    assert response.status_code == 200


def test_delete_user_unauthorized(db_setup):
    """Test function for DELETE /user/{id} 401 UNAUTHORIZED"""
    global julienMock
    response = client.put(
        "/user/" + str(julienMock["id"]),
    )
    assert response.status_code == 401


def test_delete_user_success(db_setup):
    """Test function for DELETE /user/{id} 200 OK"""
    global julienMock
    global token
    headers = {"Authorization": "Bearer {}".format(token["access_token"])}
    response = client.delete(
        "/user/" + str(julienMock["id"]),
        headers=headers,
    )
    assert response.status_code == 200
