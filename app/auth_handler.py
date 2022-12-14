import time
import jwt
from jwt import DecodeError
from pydantic import BaseModel, ValidationError
from config import JWT_SECRET, JWT_ALGORITHM

class TokenData(BaseModel):
    user_id : int
    expires : int
    company_id : int
    role : str

    def is_valid(self):
        # allow tokens without expire date for testing
        return self.expires is not None and (self.expires == -1 or self.expires >= time.time())

    @staticmethod
    def from_token(token : str):

        decoded_token = TokenData._decode_jwt(token)
        if decoded_token is None:
            return None

        try:
            parsed_token = TokenData.parse_obj(decoded_token)
            if not parsed_token.is_valid():
                return None
            return parsed_token
        except ValidationError:
            return None

    @staticmethod
    def _decode_jwt(token: str):
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded_token
        except DecodeError:
            return None

    def to_token(self):
        return jwt.encode(self.dict(), JWT_SECRET, algorithm=JWT_ALGORITHM)
