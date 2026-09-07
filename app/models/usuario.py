from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    rol = Column(String, default="customer", nullable=False)

    acepto_tratamiento = Column(Boolean, default=False, nullable=False)
    fecha_consentimiento = Column(DateTime(timezone=True))