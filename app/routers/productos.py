from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.schemas.producto import Producto
from app.database import get_db
from app import models


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.get("", response_model=List[Producto])
def obtener_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()


@router.post("", response_model=Producto)
def crear_producto(
    producto: Producto,
    db: Session = Depends(get_db)
):
    nuevo_producto = models.Producto(
        id=producto.id,
        nombre=producto.nombre,
        precio_final=producto.precio_final,
        cuotas_cantidad=producto.cuotas_cantidad,
        cuotas_valor=producto.cuotas_valor,
        garantia_meses=producto.garantia_meses
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return nuevo_producto