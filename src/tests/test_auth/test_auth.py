import pytest

from src.app.utils.token import auth_token
from src.tests.conftest import (
    TestClient,
    client,
    first_user_data,
    second_user_data,
    user_data,
    admin_data,
)

auth_route = "/api/v1/auth"


def test_root(client):
    client: TestClient = client
    res = client.get("/")
    assert res.json().get("message") == "Welcome to FinBanker"
    assert res.status_code == 200


def test_registration(client):
    client: TestClient = client
    res = client.post(f"{auth_route}/register/", json=user_data)
    assert res.json().get("message") == "Registration Successful"

    assert res.json().get("data")["email"] == user_data["email"]
    assert res.status_code == 201


def test_admin_registration(client):
    client: TestClient = client
    res = client.post(f"{auth_route}/register/admin/", json=admin_data)
    print(res.text)

    assert res.json().get("message") == "Registration Successful"
    assert res.json().get("data")["email"] == admin_data["email"]
    assert res.status_code == 201


def test_login(client, first_user):
    client: TestClient = client
    res = client.post(
        f"{auth_route}/login/",
        data={"username": first_user["email"], "password": first_user["password"]},
    )
    assert res.status_code == 200
    assert res.json().get("message") == "Login Successful"
    data = res.json().get("data")
    assert data["data"]["email"] == first_user_data["email"]


def test_fail_me(first_user, client):
    client: TestClient = client
    res = client.get(f"{auth_route}/me/")

    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"


def test_me(first_auth_client):
    client: TestClient = first_auth_client

    res = client.get(f"{auth_route}/me/")

    assert res.status_code == 200
    assert res.json().get("message") == "Me Data"
    assert res.json().get("data")["email"] == first_user_data["email"]


def test_update(first_auth_client):
    client: TestClient = first_auth_client

    res = client.patch(
        f"{auth_route}/update/",
        json={"first_name": "name_change", "last_name": "change_name"},
    )
    assert res.status_code == 200
    assert res.json().get("data")["first_name"] == "name_change"


def test_delete(first_auth_client):
    client: TestClient = first_auth_client

    res = client.delete(f"{auth_route}/delete/")
    assert res.status_code == 204


def test_auth_refresh(client, first_user_login):
    client: TestClient = client
    client.headers = {
        **client.headers,
        "Refresh-Tok": first_user_login["refresh_token"]["token"],
    }
    res = client.get("/api/v1/auth/refresh/")

    assert res.status_code == 200
    assert type(res.json().get("token")) == str
    assert res.json().get("message") == "New access token created successfully"


def test_password_change(first_auth_client, first_user):
    client: TestClient = first_auth_client
    res = client.patch(
        f"{auth_route}/change-password/",
        json={"password": "new_password", "old_password": first_user["password"]},
    )
    assert res.status_code == 200
    assert res.json().get("message") == "Password changed successfully"


def test_all_users(admin_auth_client, first_user, second_user):
    client: TestClient = admin_auth_client

    res = client.get(f"{auth_route}/all-users/")
    assert res.status_code == 200
    assert res.json().get("message") == "all users on fin-banker retrieved successfully"


def test_failed_all_users(first_auth_client, first_user, second_user):
    client: TestClient = first_auth_client

    res = client.get(f"{auth_route}/all-users/")
    assert res.status_code == 403
    assert (
        res.json().get("detail")
        == "user does not have the permission to carry out such action"
    )
