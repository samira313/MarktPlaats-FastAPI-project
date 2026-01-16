from tests.integration.helpers import (
    ADS_URL,
    unique_username,
    register_and_login,
    create_ad,
)


def test_create_ad_requires_auth(client):
    res = create_ad(client)
    assert res.status_code in (401, 403), res.text


def test_update_ad_requires_auth(client):
    headers = register_and_login(client, unique_username("u1"), "pass123")
    created = create_ad(client, headers=headers)
    assert created.status_code in (200, 201), created.text
    ad_id = created.json()["id"]

    res = client.patch(f"{ADS_URL}{ad_id}", json={"title": "New"})
    assert res.status_code in (401, 403), res.text


def test_delete_ad_requires_auth(client):
    headers = register_and_login(client, unique_username("u1"), "pass123")
    created = create_ad(client, headers=headers)
    assert created.status_code in (200, 201), created.text
    ad_id = created.json()["id"]

    res = client.delete(f"{ADS_URL}{ad_id}")
    assert res.status_code in (401, 403), res.text


def test_public_list_ads(client):
    res = client.get(ADS_URL)
    assert res.status_code == 200, res.text
    assert isinstance(res.json(), list)


def test_public_get_ad_by_id_404(client):
    res = client.get(f"{ADS_URL}999999999")
    assert res.status_code == 404, res.text


def test_crud_flow_owner(client):
    headers = register_and_login(client, unique_username("owner"), "pass123")

    created = create_ad(client, headers=headers, payload={"title": "Laptop", "price": 50, "category": ["tech"]})
    assert created.status_code in (200, 201), created.text
    ad_id = created.json()["id"]

    one = client.get(f"{ADS_URL}{ad_id}")
    assert one.status_code == 200, one.text
    assert one.json()["id"] == ad_id

    upd = client.patch(f"{ADS_URL}{ad_id}", headers=headers, json={"title": "Updated"})
    assert upd.status_code == 200, upd.text
    assert upd.json()["title"] == "Updated"

    d = client.delete(f"{ADS_URL}{ad_id}", headers=headers)
    assert d.status_code in (200, 204), d.text

    gone = client.get(f"{ADS_URL}{ad_id}")
    assert gone.status_code == 404, gone.text


def test_update_forbidden_for_other_user(client):
    owner_headers = register_and_login(client, unique_username("owner"), "pass123")
    created = create_ad(client, headers=owner_headers)
    assert created.status_code in (200, 201), created.text
    ad_id = created.json()["id"]

    other_headers = register_and_login(client, unique_username("other"), "pass123")
    upd = client.patch(f"{ADS_URL}{ad_id}", headers=other_headers, json={"title": "Hacked"})
    assert upd.status_code == 403, upd.text


def test_delete_forbidden_for_other_user(client):
    owner_headers = register_and_login(client, unique_username("owner"), "pass123")
    created = create_ad(client, headers=owner_headers)
    assert created.status_code in (200, 201), created.text
    ad_id = created.json()["id"]

    other_headers = register_and_login(client, unique_username("other"), "pass123")
    d = client.delete(f"{ADS_URL}{ad_id}", headers=other_headers)
    assert d.status_code == 403, d.text
