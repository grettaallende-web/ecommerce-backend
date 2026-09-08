from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoOut
from app.services import pedidos as pedido_service


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post("/", response_model=PedidoOut, status_code=201)
def checkout(
    datos: PedidoCreate,
    usuario=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return pedido_service.crear_pedido(
        db=db,
        usuario=usuario,
        datos=datos
    )


@router.get("/mios", response_model=list[PedidoOut])
def mis_pedidos(
    usuario=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return (
        db.query(Pedido)
        .filter(Pedido.usuario_id == usuario.id)
        .order_by(Pedido.creado_en.desc())
        .all()
    )


@router.get("/{pedido_id}", response_model=PedidoOut)
def detalle(
    pedido_id: int,
    usuario=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if pedido is None or (
        pedido.usuario_id != usuario.id
        and usuario.rol != "admin"
    ):
        raise HTTPException(
            status_code=404,
            detail="No existe ese pedido"
        )

    return pedido