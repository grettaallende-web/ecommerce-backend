from app import models
from app.schemas.producto import ProductoCreate


def crear_producto(db, producto: ProductoCreate):
    nuevo = models.Producto(**producto.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


def listar_productos(
    db,
    skip: int = 0,
    limit: int = 10,
    nombre: str | None = None,
    precio_max: float | None = None
):
    query = db.query(models.Producto)

    if nombre:
        query = query.filter(
            models.Producto.nombre.ilike(f"%{nombre}%")
        )

    if precio_max is not None:
        query = query.filter(
            models.Producto.precio_final <= precio_max
        )

    return query.offset(skip).limit(limit).all()