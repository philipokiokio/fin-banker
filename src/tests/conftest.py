import pytest
from fastapi.testclient import TestClient

from src.app import main
from src.app.config import test_status
from src.app.database import Base, TestSessionLocal, test_engine
from src.app.utils.token import gen_token
from src.auth.oauth import create_access_token, create_refresh_token

# Test SQLAlchemy DBURL


@pytest.fixture
def table_control():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)


@pytest.fixture
def client(table_control):
    try:
        yield TestClient(main.app)
    finally:
        TestSessionLocal.close()


user_data = {
    "email": "test@gmail.com",
    "password": "anotherday",
    "first_name": "Philip",
    "last_name": "thebackend",
    "username": "regin",
    "is_admin": False,
}


first_user_data = {
    "email": "tester@gmail.com",
    "password": "anotherday",
    "first_name": "Philip",
    "username": "reg",
    "last_name": "thebackend",
    "is_admin": False,
}

second_user_data = {
    "email": "test@mail.com",
    "password": "anotherday",
    "first_name": "Philip",
    "last_name": "thebackend",
    "username": "regina",
    "is_admin": False,
}

admin_data = {
    "email": "admin@mail.com",
    "password": "anotherday",
    "first_name": "Philip",
    "last_name": "thebackend",
    "username": "reginaldo",
    "is_admin": True,
}


# CREATING FIRST USER
@pytest.fixture
def first_user(client):
    client: TestClient = client
    res = client.post("/api/v1/auth/register/", json=first_user_data)

    assert res.status_code == 201
    new_user = res.json()["data"]
    new_user["password"] = first_user_data["password"]
    return new_user


# CREATING SECOND USER
@pytest.fixture
def second_user(client):
    client: TestClient = client
    res = client.post("/api/v1/auth/register/", json=second_user_data)

    assert res.status_code == 201
    new_user = res.json()["data"]
    new_user["password"] = second_user_data["password"]
    return new_user


# CREATING ADMIN
@pytest.fixture
def admin_user(client):
    client: TestClient = client
    res = client.post("/api/v1/auth/register/admin/", json=admin_data)

    assert res.status_code == 201
    new_user = res.json()["data"]
    new_user["password"] = admin_data["password"]
    return new_user


@pytest.fixture
def first_user_login(client, first_user):
    client: TestClient = client
    res = client.post(
        "/api/v1/auth/login/",
        data={"username": first_user["email"], "password": first_user["password"]},
    )
    assert res.status_code == 200
    return res.json().get("data")


# Auth Clients for refresh and access token for the first user


@pytest.fixture
def first_user_access(first_user):
    access_token = create_access_token(first_user)
    return access_token


@pytest.fixture
def first_user_refresh(first_user):
    data = {"email": first_user["email"]}
    refresh_token = create_refresh_token(data)
    return refresh_token


@pytest.fixture
def first_auth_client(client, first_user_access):
    client: TestClient = client
    client.headers = {"Authorization": f"Bearer {first_user_access}"}
    return client


@pytest.fixture
def secnd_user_access(second_user):
    access_token = create_access_token(second_user)
    return access_token


@pytest.fixture
def secnd_auth_client(client, secnd_user_access):
    client: TestClient = client
    client.headers = {"Authorization": f"Bearer {secnd_user_access}"}
    return client


@pytest.fixture
def admin_access(admin_user):
    return create_access_token(admin_user)


@pytest.fixture
def admin_auth_client(client, admin_access):
    client: TestClient = client
    client.headers = {"Authorization": f"Bearer {admin_access}"}
    return client


first_tranzaction = {"amount": "100.00", "reciever_username": "regina"}
second_tranzaction = {"amount": " 200.00", "reciever_username": "reg"}

transaction = "/api/v1/transaction"


@pytest.fixture
def first_user_transfer(first_auth_client, second_user):
    client: TestClient = first_auth_client
    first_tranzaction["amount"] = "100.00"
    res = client.post(
        f"{transaction}/transfer/",
        params={"amount": first_tranzaction["amount"]},
        json=first_tranzaction,
    )
    return res.json().get("data")


@pytest.fixture
def second_user_transfer(secnd_auth_client, first_user):
    client: TestClient = secnd_auth_client
    res = client.post(
        f"{transaction}/transfer/",
        params={"amount": second_tranzaction["amount"]},
        json=second_tranzaction,
    )
    # print(res.text)
    return res.json().get("data")


@pytest.fixture
def update_transaction_yes(client, secnd_user_access, first_user_transfer):
    tranzact_id = first_user_transfer["tranzact_id"]

    client: TestClient = client
    client.headers = {"Authorization": f"Bearer {secnd_user_access}"}

    res = client.patch(
        f"{transaction}/{tranzact_id}/update/", json={"is_accepted": True}
    )
    return res.json().get("data")


@pytest.fixture
def update_transaction_no(secnd_auth_client, first_user_transfer):
    tranzact_id = first_user_transfer["tranzact_id"]

    client: TestClient = secnd_auth_client
    res = client.patch(
        f"{transaction}/{tranzact_id}/update/", json={"is_accepted": False}
    )
    return res.json().get("data")


@pytest.fixture
def revert_transaction_successfully(client, admin_access, update_transaction_yes):
    tranzact_id = update_transaction_yes["tranzact_id"]

    client: TestClient = client
    client.headers = {"Authorization": f"Bearer {admin_access}"}

    res = client.patch(
        f"{transaction}/{tranzact_id}/revert/",
    )
    print(res.text)
    return res.json().get("data")
