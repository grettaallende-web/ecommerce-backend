from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel

from app import models
from app.database import SessionLocal
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.core.security import (
    hash_password,
    verificar_password,
    crear_token
)
from app.core.config import settings
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UsuarioOut)
def registrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    usuario_existente = db.query(models.Usuario).filter(
        models.Usuario.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )

    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        hashed_password=hash_password(usuario.password),
        rol="customer",
        acepto_tratamiento=True,
        fecha_consentimiento=datetime.now(timezone.utc)
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == form_data.username
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Datos incorrectos"
        )

    if not verificar_password(
        form_data.password,
        usuario.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Datos incorrectos"
        )

    access_token = crear_token(
        email=usuario.email,
        rol=usuario.rol,
        minutos=settings.ACCESS_MIN,
        tipo="access"
    )

    refresh_token = crear_token(
        email=usuario.email,
        rol=usuario.rol,
        minutos=settings.REFRESH_MIN,
        tipo="refresh"
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh")
def refresh_token(
    datos: RefreshRequest,
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            datos.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("tipo") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    nuevo_access_token = crear_token(
        email=usuario.email,
        rol=usuario.rol,
        minutos=settings.ACCESS_MIN,
        tipo="access"
    )

    nuevo_refresh_token = crear_token(
        email=usuario.email,
        rol=usuario.rol,
        minutos=settings.REFRESH_MIN,
        tipo="refresh"
    )

    return {
        "access_token": nuevo_access_token,
        "refresh_token": nuevo_refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UsuarioOut)
def obtener_usuario_actual(
    usuario=Depends(get_current_user)
):
    return usuario