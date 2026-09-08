from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class ItemPedido(Base):
    __tablename__ = "items_pedido"

    id = Column(Integer, primary_key=True, index=True)

    pedido_id = Column(
        Integer,
        ForeignKey("pedidos.id"),
        nullable=False
    )

    producto_id = Column(
        Integer,
        ForeignKey("productos.id"),
        nullable=False
    )

    cantidad = Column(
        Integer,
        nullable=False
    )

    precio_unitario = Column(
        Numeric(12, 2),
        nullable=False
    )

    pedido = relationship(
        "Pedido",
        back_populates="items"
    )

    producto = relationship("Producto")