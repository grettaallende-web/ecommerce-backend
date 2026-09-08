from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal


class ItemIn(BaseModel):
    producto_id: int
    cantidad: int = Field(gt=0)


class PedidoCreate(BaseModel):
    items: list[ItemIn] = Field(min_length=1)


class ItemOut(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal

    class Config:
        from_attributes = True


class PedidoOut(BaseModel):
    id: int
    estado: str
    total: Decimal
    creado_en: datetime
    items: list[ItemOut]

    class Config:
        from_attributes = True