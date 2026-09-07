from pydantic import BaseModel, EmailStr, Field, field_validator


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str = Field(min_length=8)
    acepto_tratamiento: bool

    @field_validator("acepto_tratamiento")
    @classmethod
    def validar_consentimiento(cls, valor):
        if not valor:
            raise ValueError("Sin consentimiento no hay cuenta")
        return valor


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str

    class Config:
        from_attributes = True