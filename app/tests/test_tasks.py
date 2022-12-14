import time

from main import app
from auth_handler import TokenData
from fastapi.testclient import TestClient

test_client = TestClient(app)

def test_check_auth():
    # check authentication

    token = TokenData(
        user_id=1,
        expires=-1,
        company_id=0,
        role="admin",
    )
    token_data = token.to_token()
    response = test_client.post("/api/tasks/get-tasks/", json={'authorization' : token_data})
    assert response.status_code == 200