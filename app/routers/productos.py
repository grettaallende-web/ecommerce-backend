from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.producto import ProductoOut
from app.services import productos


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.get("/", response_model=list[ProductoOut])
def listar_productos(
    skip: int = 0,
    limit: int = 12,
    nombre: str | None = None,
    precio_max: float | None = None,
    db: Session = Depends(get_db)
):
    return productos.listar_productos(
        db=db,
        skip=skip,
        limit=limit,
        nombre=nombre,
        precio_max=precio_max
    )


@router.get("/{producto_id}", response_model=ProductoOut)
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    producto = productos.obtener_producto(db, producto_id)

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto