import pytest


@pytest.mark.asyncio
async def test_admin_salary_import(client, admin_token, monkeypatch):
    async def mock_import(db):
        return None

    monkeypatch.setattr(
        "app.api.routes.admin_import.run_salary_import",
        mock_import
    )

    response = await client.post(
        "/admin/import/salary",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_non_admin_forbidden(client, user_token):
    response = await client.post(
        "/admin/import/salary",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403
