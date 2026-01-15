import uuid

def test_get_messages_without_token(client):
    """
    Requesting GET /messages/ without authentication
    should be rejected with 401 or 403.
    """
    res = client.get("/messages/")
    assert res.status_code in (401, 403)


def test_get_messages_with_token(client):
    """
    Full integration flow:
    1. Register a new user
    2. Login and receive access token
    3. Call GET /messages/ with Authorization header
    """
    # Generate unique username to avoid collisions between test runs
    username = f"user_{uuid.uuid4().hex[:8]}"
    password = "pass123"

    # 1 Register
    reg_res = client.post(
        "/users/register",
        json={"username": username, "password": password}
    )
    assert reg_res.status_code in (200, 201), reg_res.text

    # 2 Login (OAuth2 form data)
    login_res = client.post(
        "/users/login",
        data={"username": username, "password": password}
    )
    assert login_res.status_code == 200, login_res.text

    token = login_res.json()["access_token"]

    # 3 Authenticated request
    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/messages/", headers=headers)

    # 200: messages returned
    # 422: valid request but missing required query params (e.g. with_user_id)
    assert res.status_code in (200, 422), res.text
