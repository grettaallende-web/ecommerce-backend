from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.producto import Producto


def crear_pedido(db: Session, usuario, datos):

    try:
        pedido = Pedido(
            usuario_id=usuario.id,
            estado="pendiente"
        )

        total = Decimal("0")

        for item in datos.items:

            producto = (
                db.query(Producto)
                .filter(Producto.id == item.producto_id)
                .with_for_update()
                .first()
            )

            if producto is None:
                raise HTTPException(
                    status_code=404,
                    detail="Producto inexistente"
                )

            if producto.stock < item.cantidad:
                raise HTTPException(
                    status_code=409,
                    detail=f"Sin stock de {producto.nombre}: quedan {producto.stock}"
                )

            producto.stock -= item.cantidad

            precio = Decimal(str(producto.precio_final))

            total += precio * item.cantidad

            pedido.items.append(
                ItemPedido(
                    producto_id=producto.id,
                    cantidad=item.cantidad,
                    precio_unitario=precio
                )
            )

        pedido.total = total

        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        return pedido

    except Exception:
        db.rollback()
        raise