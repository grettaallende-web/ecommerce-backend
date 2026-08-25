from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers.productos import router as productos_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API E-Commerce Argentino",
    description="API profesional para e-commerce en la República Argentina.",
    version="1.0.0",
)


@app.get("/")
async def read_root():
    return {
        "mensaje": "Bienvenido a la API oficial del E-Commerce Argentino",
        "estado": "Operativo",
        "version": "1.0.0",
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


app.include_router(productos_router)