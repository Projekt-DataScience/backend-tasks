from main import app
from fastapi.testclient import TestClient

test_client = TestClient(app)
from helpers.auth import login

def test_check_auth():
    token = login()
    print(token)
    response = test_client.get(
        "/api/tasks/get-tasks/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200