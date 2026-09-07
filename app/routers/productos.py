from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_admin
from app.schemas.producto import ProductoCreate, ProductoOut
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


@router.post(
    "/",
    response_model=ProductoOut,
    status_code=status.HTTP_201_CREATED
)
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_admin)
):
    return productos.crear_producto(
        db=db,
        producto=producto
    )


@router.put(
    "/{producto_id}",
    response_model=ProductoOut
)
def actualizar_producto(
    producto_id: int,
    producto: ProductoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_admin)
):
    producto_existente = productos.obtener_producto(
        db,
        producto_id
    )

    if not producto_existente:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto_existente.nombre = producto.nombre
    producto_existente.precio_final = producto.precio_final
    producto_existente.cuotas_cantidad = producto.cuotas_cantidad
    producto_existente.cuotas_valor = producto.cuotas_valor
    producto_existente.garantia_meses = producto.garantia_meses
    producto_existente.stock = producto.stock

    db.commit()
    db.refresh(producto_existente)

    return producto_existente


@router.delete(
    "/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_admin)
):
    producto = productos.obtener_producto(
        db,
        producto_id
    )

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    db.delete(producto)
    db.commit()

    return None
