from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import categorias, productos, proveedores, clientes, documentos, movimientos
from . import models, database

# Crear tablas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],  # 👈 dominio de tu frontend Astro
    allow_credentials=True,
    allow_methods=["*"],  # permite todos los métodos: GET, POST, PUT, DELETE
    allow_headers=["*"],  # permite todos los headers (ej: Authorization)
)

# Incluir routers
app.include_router(categorias.router)
app.include_router(productos.router)
app.include_router(proveedores.router)
app.include_router(clientes.router)
app.include_router(documentos.router)
app.include_router(movimientos.router)
