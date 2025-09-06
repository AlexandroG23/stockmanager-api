from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas, database

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"],
)

# Dependencia para obtener la sesión de BD
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# 📌 ENDPOINTS CATEGORÍA
# =========================

# Crear Categoria
@router.post("/", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db=db, categoria=categoria)

# Listar Categorias
@router.get("/", response_model=List[schemas.Categoria])
def listar_categorias(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_categorias(db, skip=skip, limit=limit)

# Obtener una categoria por ID
@router.get("/{categoria_id}", response_model=schemas.Categoria)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = crud.get_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return db_categoria

# DELETE (seguro: no elimina si hay productos asociados)
@router.delete("/{categoria_id}", response_model=schemas.Categoria)
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    result = crud.delete_categoria(db, categoria_id=categoria_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if result == "CONFLICT":
        raise HTTPException(status_code=409, detail="No se puede eliminar la categoría porque tiene productos asociados")
    return result

# PUT (actualización total)
@router.put("/{categoria_id}", response_model=schemas.Categoria)
def update_categoria(categoria_id: int, categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = crud.update_categoria(db, categoria_id=categoria_id, categoria_update=categoria)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

# PATCH (actualización parcial)
@router.patch("/{categoria_id}", response_model=schemas.Categoria)
def patch_categoria(categoria_id: int, categoria_patch: dict, db: Session = Depends(get_db)):
    db_categoria = crud.patch_categoria(db, categoria_id=categoria_id, categoria_patch=categoria_patch)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria