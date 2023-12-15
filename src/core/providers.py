import jwt
from core.settings import SECRET_KEY

class JWTProvider:
    @staticmethod
    async def decode(token: str):
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    
    @staticmethod
    async def encode(payload: dict):
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')