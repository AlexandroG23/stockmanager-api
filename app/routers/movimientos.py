from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from sqlalchemy.orm import joinedload

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/movimientos",
    tags=["Movimientos"]
)

# =========================
# 📌 Crear Movimiento
# =========================
@router.post("/", response_model=schemas.Movimiento)
def create_movimiento(movimiento: schemas.MovimientoCreate, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == movimiento.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Ajustar stock automáticamente
    if movimiento.tipo == "entrada":
        producto.stock_actual += movimiento.cantidad
    elif movimiento.tipo == "salida":
        if producto.stock_actual < movimiento.cantidad:
            raise HTTPException(status_code=400, detail="Stock insuficiente")
        producto.stock_actual -= movimiento.cantidad
    else:
        raise HTTPException(status_code=400, detail="Tipo de movimiento inválido")

    db.add(producto)

    db_movimiento = models.Movimiento(
        producto_id=movimiento.producto_id,
        tipo=movimiento.tipo,
        cantidad=movimiento.cantidad,
        fecha=datetime.utcnow()
    )
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento


# =========================
# 📌 Listar Movimientos
# =========================
@router.get("/", response_model=List[schemas.Movimiento])
def get_movimientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movimientos = (
        db.query(models.Movimiento)
        .options(joinedload(models.Movimiento.producto))  # 👈 aquí cargamos el producto
        .offset(skip)
        .limit(limit)
        .all()
    )
    return movimientos


# =========================
# 📌 Obtener Movimientos por Producto
# =========================
@router.get("/producto/{producto_id}", response_model=List[schemas.Movimiento])
def get_movimientos_producto(producto_id: int, db: Session = Depends(get_db)):
    return db.query(models.Movimiento).filter(models.Movimiento.producto_id == producto_id).all()


# =========================
# 📌 Filtrar Movimientos por Fecha y Tipo
# =========================
@router.get("/reportes", response_model=List[schemas.Movimiento])
def reporte_movimientos(
        tipo: str = None,  # "entrada" o "salida"
        fecha_inicio: datetime = None,
        fecha_fin: datetime = None,
        db: Session = Depends(get_db)
):
    query = db.query(models.Movimiento)
    if tipo:
        query = query.filter(models.Movimiento.tipo == tipo)
    if fecha_inicio:
        query = query.filter(models.Movimiento.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(models.Movimiento.fecha <= fecha_fin)
    return query.all()