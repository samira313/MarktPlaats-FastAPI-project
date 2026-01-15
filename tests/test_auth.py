import uuid


# Helper functions

def unique_username(prefix: str = "user") -> str:
    """
    Generate a unique username to avoid collisions between test runs.
    """
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def register_user(client, username: str, password: str):
    """
    Helper: Register a user using JSON body.
    """
    return client.post(
        "/users/register",
        json={"username": username, "password": password},
    )


def login_user(client, username: str, password: str):
    """
    Helper: Login using OAuth2 form data (NOT JSON).
    FastAPI's OAuth2PasswordRequestForm expects application/x-www-form-urlencoded.
    """
    return client.post(
        "/users/login",
        data={"username": username, "password": password},
    )


def auth_headers(token: str) -> dict:
    """
    Helper: Build Authorization header from access token.
    """
    return {"Authorization": f"Bearer {token}"}


def register_and_login(client, username: str, password: str) -> str:
    """
    Helper: Register + login and return access token.
    """
    reg = register_user(client, username, password)
    assert reg.status_code in (200, 201), reg.text

    login = login_user(client, username, password)
    assert login.status_code == 200, login.text

    data = login.json()
    assert "access_token" in data, f"Missing access_token in response: {data}"
    return data["access_token"]


# Tests: Register

def test_register_success(client):
    """
    Registering a new user should succeed.
    """
    username = unique_username("newuser")
    password = "pass123"

    res = register_user(client, username, password)

    assert res.status_code in (200, 201), res.text
    assert isinstance(res.json(), dict)


def test_register_duplicate_username(client):
    """
    Registering the same username twice should fail (400 or 409).
    """
    username = unique_username("dupuser")
    password = "pass123"

    first = register_user(client, username, password)
    assert first.status_code in (200, 201), first.text

    second = register_user(client, username, password)
    assert second.status_code in (400, 409), second.text


# Tests: Login

def test_login_success_returns_token(client):
    """
    Logging in with valid credentials should return an access token.
    """
    username = unique_username("loginuser")
    password = "pass123"

    # Ensure user exists
    reg = register_user(client, username, password)
    assert reg.status_code in (200, 201), reg.text

    res = login_user(client, username, password)
    assert res.status_code == 200, res.text

    data = res.json()
    assert "access_token" in data
    assert data.get("token_type") == "bearer"


def test_login_wrong_password_fails(client):
    """
    Logging in with a wrong password should fail (401 typically).
    """
    username = unique_username("wrongpw")
    password = "pass123"

    reg = register_user(client, username, password)
    assert reg.status_code in (200, 201), reg.text

    res = login_user(client, username, "WRONG_PASSWORD")
    assert res.status_code in (400, 401), res.text



# Tests: Logout

def test_logout_requires_token(client):
    """
    Logout without an Authorization header should be rejected.
    """
    res = client.post("/users/logout")
    assert res.status_code in (401, 403), res.text


def test_logout_invalidates_token_if_blacklist_used(client):
    """
    If the backend uses a token blacklist, after logout the same token
    should no longer work for protected endpoints (e.g. /users/me).

    Note: This test assumes your /users/me endpoint is protected and exists.
    """
    username = unique_username("logoutuser")
    password = "pass123"

    token = register_and_login(client, username, password)
    headers = auth_headers(token)

    # Logout
    out = client.post("/users/logout", headers=headers)
    assert out.status_code in (200, 204), out.text

    # After logout, token should be invalid for protected endpoints
    me = client.get("/users/me", headers=headers)
    assert me.status_code in (401, 403), me.text
