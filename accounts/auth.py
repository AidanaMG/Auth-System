import jwt
import datetime
from django.conf import settings
import bcrypt



def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        "iat": datetime.datetime.now(datetime.timezone.utc),  
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    return payload

def hash_password(raw_password):
    password_bytes = raw_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")  


def check_password(raw_password, hashed_password):
    password_bytes = raw_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)