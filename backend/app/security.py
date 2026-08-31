from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(username: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode({"sub": username, "exp": expires}, settings.jwt_secret, algorithm="HS256")

def decode_username(token: str) -> str | None:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"]).get("sub")
    except JWTError:
        return None
