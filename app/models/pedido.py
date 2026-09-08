from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    total = Column(Numeric(12, 2), nullable=False, default=0)

    creado_en = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    estado = Column(
        String,
        default="pendiente",
        nullable=False
    )

    usuario = relationship("Usuario")

    items = relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )