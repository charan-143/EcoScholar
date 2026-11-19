import os
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash

_passwords = PasswordHash.recommended()
ALGORITHM = "HS256"

def _secret():
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        if os.getenv("ENVIRONMENT", "development") == "production":
            raise RuntimeError("JWT_SECRET_KEY must be configured in production")
        secret = "dev-only-change-this-secret-before-deployment"
    return secret

def hash_password(password: str) -> str:
    return _passwords.hash(password)

def verify_password(password: str, encoded: str) -> bool:
    return _passwords.verify(password, encoded)

def create_access_token(user_id: int, role: str) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "role": role, "iat": now, "exp": now + timedelta(hours=12)}, _secret(), algorithm=ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(token, _secret(), algorithms=[ALGORITHM])
