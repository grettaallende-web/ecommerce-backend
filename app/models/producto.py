from sqlalchemy import Column, Integer, String, Float

from app.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    precio_final = Column(Float)
    cuotas_cantidad = Column(Integer)
    cuotas_valor = Column(Float)
    garantia_meses = Column(Integer)