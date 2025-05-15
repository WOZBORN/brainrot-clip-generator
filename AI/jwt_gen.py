import time
import jwt

def encode_jwt_token(ak: str, sk: str) -> str:
    """
    Создаёт JWT с issuer=ak, сроком жизни 30 мин и nbf=current_time-5s
    """
    headers = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    payload = {
        "iss": ak,
        "exp": now + 1800,  # истекает через 30 минут
        "nbf": now - 5      # начинает действовать за 5 секунд до текущего времени
    }
    # PyJWT>=2.0 encode возвращает строку
    token = jwt.encode(payload, sk, algorithm="HS256", headers=headers)
    return token