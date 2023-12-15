import jwt
from core.settings import SECRET_KEY

class JWTProvider:
    """
    Класс для работы с JSON Web Tokens (JWT).
    """

    @staticmethod
    async def decode(token: str):
        """
        Декодирует JWT токен.

        :param token: JWT токен для декодирования.
        :return: Словарь данных, содержащихся в декодированном токене.
        """

        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    
    @staticmethod
    async def encode(payload: dict):
        """
        Кодирует данные в JWT токен.

        :param payload: Словарь данных, который будет закодирован в токен.
        :return: Строка с закодированным JWT токеном.
        """

        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')