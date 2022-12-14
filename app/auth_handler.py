import time
import jwt
from jwt import DecodeError
from pydantic import BaseModel
from config import JWT_SECRET, JWT_ALGORITHM

class TokenData(BaseModel):
    user_id : int
    expires : int
    company_id : int
    role : str
    token_type: str

    @staticmethod
    def from_token(token : str):
        decoded_token = TokenData._decode_jwt(token)

        if decoded_token is None:
            return None

        return TokenData.parse_raw(decoded_token)


    @staticmethod
    def _decode_jwt(token: str):
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except DecodeError:
            return None

    def to_token(self):
        return jwt.encode(self.json(), JWT_SECRET, algorithm=JWT_ALGORITHM)
