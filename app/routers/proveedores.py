from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores"],
)

# Crear
@router.post("/", response_model=schemas.Proveedor)
def create_proveedor(proveedor: schemas.ProveedorCreate, db: Session = Depends(get_db)):
    return crud.create_proveedor(db, proveedor)

# Listar
@router.get("/", response_model=List[schemas.Proveedor])
def get_proveedores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_proveedores(db, skip=skip, limit=limit)

# Obtener uno
@router.get("/{proveedor_id}", response_model=schemas.Proveedor)
def get_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = crud.get_proveedor(db, proveedor_id)
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

# Actualizar
@router.put("/{proveedor_id}", response_model=schemas.Proveedor)
def update_proveedor(proveedor_id: int, proveedor: schemas.ProveedorCreate, db: Session = Depends(get_db)):
    db_proveedor = crud.update_proveedor(db, proveedor_id, proveedor)
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_proveedor

@router.patch("/{proveedor_id}", response_model=schemas.Proveedor)
def update_proveedor_partial(
    proveedor_id: int,
    proveedor_update: schemas.ProveedorUpdate,  # schema con todos los campos opcionales
    db: Session = Depends(get_db)
):
    db_proveedor = db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    update_data = proveedor_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_proveedor, key, value)

    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

# Eliminar
@router.delete("/{proveedor_id}")
def delete_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    db_proveedor = crud.delete_proveedor(db, proveedor_id)
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return {"message": f"Proveedor con ID {proveedor_id} eliminado correctamente"}