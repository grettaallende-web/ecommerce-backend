from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.schemas.producto import ProductoCreate, ProductoOut
from app.database import get_db
from app.services import productos as productos_service


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.get("", response_model=List[ProductoOut])
def obtener_productos(
    skip: int = 0,
    limit: int = 10,
    nombre: str | None = None,
    precio_max: float | None = None,
    db: Session = Depends(get_db)
):
    return productos_service.listar_productos(
        db,
        skip=skip,
        limit=limit,
        nombre=nombre,
        precio_max=precio_max
    )


@router.post("", response_model=ProductoOut)
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db)
):
    return productos_service.crear_producto(db, producto)