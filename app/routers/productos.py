from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, database

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

# Dependencia para la BD
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 📌 Endpoints
# =========================

# Crear producto
@router.post("/", response_model=schemas.Producto)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db=db, producto=producto)

# Listar productos
@router.get("/", response_model=List[schemas.Producto])
def get_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_productos(db, skip=skip, limit=limit)

# Obtener producto por ID
@router.get("/{producto_id}", response_model=schemas.Producto)
def get_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, producto_id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# DELETE producto
@router.delete("/{producto_id}", status_code=200)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db, producto_id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(db_producto)
    db.commit()
    return {"message": f"Producto con ID {producto_id} eliminado correctamente"}

# PUT (actualización total)
@router.put("/{producto_id}", response_model=schemas.Producto)
def update_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = crud.update_producto(db, producto_id=producto_id, producto_update=producto)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


# PATCH (actualización parcial)
@router.patch("/{producto_id}", response_model=schemas.Producto)
def patch_producto(producto_id: int, producto_patch: dict, db: Session = Depends(get_db)):
    db_producto = crud.patch_producto(db, producto_id=producto_id, producto_patch=producto_patch)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto