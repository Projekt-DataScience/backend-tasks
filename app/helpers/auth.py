import os
import requests
from fastapi import HTTPException, status

HOSTNAME = os.environ.get("USER_MANAGEMENT_SERVICE_HOSTNAME")
PORT = os.environ.get("USER_MANAGEMENT_SERVICE_PORT")

def generate_url(path: str):
    return f"http://{HOSTNAME}:{PORT}{path}"

def validate_jwt(jwt: str):
    jwt = jwt.replace("Bearer ", "")
    PATH = "/api/user_management/validateJWT/?jwt=" + jwt
    URL = generate_url(PATH)
    print(URL)

    response = requests.post(URL)

    if response.status_code == 200:
        return response.json()["payload"]
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT")


def validate_authorization(authorization: str):
    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header not found")

    return validate_jwt(authorization)


def login():
    """
    Function should only be used for tests
    :param client: FastAPI test client
    :returns: JWT Token as string
    """
    PATH = "/api/user_management/login/"
    URL = generate_url(PATH)
    credentials = {
        "email": "josef@test.de",
        "password": "test"
    }
    print("login url", URL)

    response = requests.post(URL, json=credentials)
    print("login response", response.json())

    return response.json().get("token")
