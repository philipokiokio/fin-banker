import pytest
from src.tests.conftest import TestClient, transaction, first_tranzaction, client


def test_first_user_transfer(first_auth_client, second_user):
    client: TestClient = first_auth_client

    res = client.post(
        f"{transaction}/transfer/",
        params={"amount": first_tranzaction["amount"]},
        json=first_tranzaction,
    )

    assert res.status_code == 201
    assert res.json().get("message") == "transaction is sent successfully"


def test_first_user_nd_failed_transfer(
    first_auth_client, second_user, first_user_transfer
):
    client: TestClient = first_auth_client
    first_tranzaction_ = first_tranzaction
    first_tranzaction_["amount"] = "1000.00"
    res = client.post(
        f"{transaction}/transfer/",
        params={"amount": first_tranzaction_["amount"]},
        json=first_tranzaction_,
    )

    assert res.status_code == 400
    assert (
        res.json().get("detail")
        == "sender has insufficient balance to complete this transaction"
    )


def test_all_transactions_users(
    first_auth_client,
    first_user_transfer,
    second_user_transfer,
):
    client: TestClient = first_auth_client
    res = client.get(f"{transaction}s/")

    assert res.status_code == 200
    assert res.json().get("message") == "tranzactions returned sucessfully"
    assert len(res.json().get("data")) == 2


def test_get_transaction(first_auth_client, first_user_transfer):
    tranzact_id = first_user_transfer["tranzact_id"]
    client: TestClient = first_auth_client
    res = client.get(f"{transaction}/{tranzact_id}/")

    assert res.status_code == 200
    assert res.json().get("message") == "tranzaction retrieved successfully"


def test_get_user_balance(first_auth_client, first_user_transfer):
    client: TestClient = first_auth_client
    res = client.get("/api/v1/auth/me/")

    data = res.json().get("data")
    assert data["account"][0]["balance"] == 900.0


def test_update_transaction_transaction_failed(first_auth_client, first_user_transfer):
    tranzact_id = first_user_transfer["tranzact_id"]

    client: TestClient = first_auth_client
    res = client.patch(
        f"{transaction}/{tranzact_id}/update/", json={"is_accepted": True}
    )

    assert res.status_code == 400
    assert res.json().get("detail") == "User is not the recipient of this tranzaction"


def test_update_transaction_successfully(
    client, secnd_user_access, first_user_transfer
):
    tranzact_id = first_user_transfer["tranzact_id"]

    client: TestClient = client
    client.headers = {"Authorization": f"Bearer {secnd_user_access}"}
    res = client.patch(
        f"{transaction}/{tranzact_id}/update/", json={"is_accepted": True}
    )
    print(res.text)
    assert res.status_code == 200
    assert res.json().get("message") == "tranzaction updated successfully"


def test_update_transaction_resolved(
    secnd_auth_client, first_user_transfer, update_transaction_yes
):
    tranzact_id = first_user_transfer["tranzact_id"]

    client: TestClient = secnd_auth_client
    res = client.patch(
        f"{transaction}/{tranzact_id}/update/", json={"is_accepted": True}
    )

    assert res.status_code == 409
    assert res.json().get("detail") == "Tranzaction resolved"


def test_get_user_balance_after_settlement(first_auth_client, update_transaction_no):
    client: TestClient = first_auth_client
    res = client.get("/api/v1/auth/me/")

    data = res.json().get("data")
    assert data["account"][0]["balance"] == 1000.0


def test_get_transactions_fail(
    first_auth_client, second_user_transfer, first_user_transfer
):
    client: TestClient = first_auth_client
    res = client.get(f"{transaction}s/admin/")

    assert (
        res.json().get("detail")
        == "user does not have the permission to carry out such action"
    )
    assert res.status_code == 403


def test_get_transactions_sucess(
    client, admin_access, second_user_transfer, first_user_transfer
):
    client: TestClient = client
    client.headers = {"Authorization": f"Bearer {admin_access}"}
    res = client.get(f"{transaction}s/admin/")

    assert res.json().get("message") == "tranzactions returned sucessfully"
    assert res.status_code == 200
    assert len(res.json().get("data")) == 2


def test_revert_transaction_admin(
    client, admin_access, first_user_transfer, update_transaction_yes
):
    tranzact_id = first_user_transfer["tranzact_id"]

    client: TestClient = client
    client.headers = {"Authorization": f"Bearer {admin_access}"}

    res = client.patch(
        f"{transaction}/{tranzact_id}/revert/",
    )

    assert res.status_code == 200
    assert res.json().get("message") == "tranzaction reverted successfully"


# def test_get_user_balance_frist_settlement(
#     first_auth_client, revert_transaction_successfully
# ):
#     client: TestClient = first_auth_client
#     res = client.get("/api/v1/auth/me/")

#     data = res.json().get("data")
#     assert data["account"][0]["balance"] == 1000.0


# def test_get_user_balance_second_settlement(
#     secnd_auth_client, revert_transaction_successfully
# ):
#     client: TestClient = secnd_auth_client
#     res = client.get("/api/v1/auth/me/")

#     data = res.json().get("data")
#     assert data["account"][0]["balance"] == 1000.0
