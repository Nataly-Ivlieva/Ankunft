import pytest
import uuid


@pytest.mark.asyncio
async def test_admin_signup_and_login(client):
    email = f"admin_{uuid.uuid4()}@test.de"

    signup_data = {
        "email": email,
        "password": "securepassword",
        "role": "admin",
    }

    response = await client.post("/auth/signup", json=signup_data)
    assert response.status_code == 200

    login_data = {
        "email": email,
        "password": "securepassword",
    }

    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert response.json()["role"] == "admin"
