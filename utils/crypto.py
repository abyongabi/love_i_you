import bcrypt
from datetime import datetime, timedelta, timezone
import jwt

from utils.application_config import app_config


def hash_value(value: str) -> str:
    value_bytes: bytes = value.encode('utf-8')
    salt: bytes = bcrypt.gensalt()
    hashed_bytes: bytes = bcrypt.hashpw(value_bytes, salt)
    return hashed_bytes.decode('utf-8')


def verify_value(value: str, stored_hash: str) -> bool:
    value_bytes: bytes = value.encode('utf-8')
    hash_bytes: bytes = stored_hash.encode('utf-8')
    return bcrypt.checkpw(value_bytes, hash_bytes)


def create_access_token(payload: dict) -> str:
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=1)
    token: str = jwt.encode(
        payload,
        app_config.jwt_secret,
        algorithm="HS256"
    )
    return token