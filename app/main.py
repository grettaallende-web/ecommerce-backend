from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers.productos import router as productos_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API E-Commerce Argentino",
    description=(
        "API profesional para e-commerce en la República Argentina. "
        "Esta plataforma y todas sus transacciones comerciales se encuentran sujetas a la "
        "Ley N° 24.240 de Defensa del Consumidor y sus reglamentaciones complementarias."
    ),
    version="1.0.0",
)


@app.get("/")
async def read_root():
    return {
        "mensaje": "Bienvenido a la API oficial del E-Commerce Argentino",
        "estado": "Operativo",
        "version": "1.0.0",
        "marco_legal": {
            "normativa": "Ley N° 24.240 de Defensa del Consumidor",
            "jurisdiccion": "República Argentina",
            "nota_legal": (
                "De conformidad con el artículo 4° de la Ley 24.240, "
                "el proveedor está obligado a suministrar a los consumidores "
                "información en forma cierta, clara y detallada sobre todo lo "
                "relacionado con las características esenciales de los bienes y servicios."
            ),
        },
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc",
        },
    }


app.include_router(productos_router)