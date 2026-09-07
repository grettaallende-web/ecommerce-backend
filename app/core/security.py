from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import jwt

from app.core.config import settings


pwd = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(p: str) -> str:
    return pwd.hash(p)


def verificar_password(plano: str, hashed: str) -> bool:
    return pwd.verify(plano, hashed)


def crear_token(
    email: str,
    rol: str,
    minutos: int,
    tipo: str
) -> str:
    payload = {
        "sub": email,
        "rol": rol,
        "tipo": tipo,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=minutos),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )