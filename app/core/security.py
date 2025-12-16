import secrets
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

TOKEN_LIFETIME = timedelta(days=30)

def hash_password(password: str) -> str:
    return pwd_context.hash(password.encode("utf-8"))

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password.encode("utf-8"), hashed)

def generate_session_token() -> str:
    return secrets.token_urlsafe(32)

def token_expiration() -> datetime:
    return datetime.utcnow() + TOKEN_LIFETIME
