import uuid

REGISTER_URL = "/users/register"
LOGIN_URL = "/users/login"
ADS_URL = "/ads/"


def unique_username(prefix: str = "user") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def register_user(client, username: str, password: str):
    return client.post(
        REGISTER_URL,
        json={"username": username, "password": password},
    )


def login_user(client, username: str, password: str):
    # OAuth2 form data (NOT JSON)
    return client.post(
        LOGIN_URL,
        data={"username": username, "password": password},
    )


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def register_and_login(client, username: str, password: str) -> dict:
    reg = register_user(client, username, password)
    assert reg.status_code in (200, 201), reg.text

    login = login_user(client, username, password)
    assert login.status_code == 200, login.text

    token = login.json()["access_token"]
    return auth_headers(token)


def create_ad(client, headers: dict | None = None, payload: dict | None = None):
    payload = payload or {"title": "Phone", "price": 10, "category": ["tech"]}
    return client.post(ADS_URL, headers=headers, json=payload)
