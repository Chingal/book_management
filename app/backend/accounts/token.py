import jwt
import datetime

from django.conf import settings

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
        "iat": datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return True, payload["user_id"]
    except jwt.ExpiredSignatureError:
        return False, "El token ha expirado."
    except jwt.InvalidTokenError:
        return False, "Token inválido."
