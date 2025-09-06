from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


# =========================
# 📌 CRUD CATEGORIA
# =========================

# Crear Categoria
def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


# Listar todas las categorias
def get_categorias(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Categoria).offset(skip).limit(limit).all()

# Obtener una categoria por ID
def get_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

# Eliminar Categoria
def delete_categoria(db: Session, categoria_id: int):
    categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not categoria:
        return None

    # Revisar si hay productos vinculados
    productos_asociados = db.query(models.Producto).filter(models.Producto.categoria_id == categoria_id).all()
    if productos_asociados:
        return "CONFLICT"

    db.delete(categoria)
    db.commit()
    return categoria

# Actualizar Categoria (PUT)
def update_categoria(db: Session, categoria_id: int, categoria_update: schemas.CategoriaCreate):
    """Actualiza una categoría de manera TOTAL (PUT)"""
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not db_categoria:
        return None

    # Validar que no exista otra categoría con el mismo nombre
    existe = db.query(models.Categoria).filter(
        models.Categoria.nombre == categoria_update.nombre,
        models.Categoria.id != categoria_id
    ).first()
    if existe:
        raise ValueError("Ya existe otra categoría con ese nombre")

    for key, value in categoria_update.model_dump().items():
        setattr(db_categoria, key, value)

    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# Actualizar Categoria (PATCH)
def patch_categoria(db: Session, categoria_id: int, categoria_patch: dict):
    """Actualiza una categoría de manera PARCIAL (PATCH)"""
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if not db_categoria:
        return None

    # Validar nombre único solo si se quiere cambiar
    nuevo_nombre = categoria_patch.get("nombre")
    if nuevo_nombre:
        existe = db.query(models.Categoria).filter(
            models.Categoria.nombre == nuevo_nombre,
            models.Categoria.id != categoria_id
        ).first()
        if existe:
            raise ValueError("Ya existe otra categoría con ese nombre")

    for key, value in categoria_patch.items():
        setattr(db_categoria, key, value)

    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# =========================
# 📌 CRUD PRODUCTOS
# =========================

# Crear Producto
def create_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Listar productos
def get_productos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Producto).offset(skip).limit(limit).all()

# Obtener un producto por ID
def get_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

# Eliminar producto
def delete_producto(db: Session, producto_id: int):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        return None

    db.delete(producto)
    db.commit()
    return producto

# Actualizar Producto (PUT)
def update_producto(db: Session, producto_id: int, producto_update: schemas.ProductoCreate):
    """Actualiza un producto de manera TOTAL (PUT)"""
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not db_producto:
        return None

    for key, value in producto_update.model_dump().items():
        setattr(db_producto, key, value)

    db.commit()
    db.refresh(db_producto)
    return db_producto

# Actualizar Producto (PATCH)
def patch_producto(db: Session, producto_id: int, producto_patch: dict):
    """Actualiza un producto de manera PARCIAL (PATCH)"""
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not db_producto:
        return None

    for key, value in producto_patch.items():
        setattr(db_producto, key, value)

    db.commit()
    db.refresh(db_producto)
    return db_producto

# =========================
# 📌 CRUD PROVEEDOR
# =========================

# Crear
def create_proveedor(db: Session, proveedor: schemas.ProveedorCreate):
    db_proveedor = models.Proveedor(**proveedor.model_dump())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

# Obtener por ID
def get_proveedor(db: Session, proveedor_id: int):
    return db.query(models.Proveedor).filter(models.Proveedor.id == proveedor_id).first()

# Listar todos
def get_proveedores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Proveedor).offset(skip).limit(limit).all()

# Actualizar
def update_proveedor(db: Session, proveedor_id: int, proveedor: schemas.ProveedorCreate):
    db_proveedor = get_proveedor(db, proveedor_id)
    if not db_proveedor:
        return None
    for key, value in proveedor.model_dump().items():
        setattr(db_proveedor, key, value)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

# Eliminar
def delete_proveedor(db: Session, proveedor_id: int):
    db_proveedor = get_proveedor(db, proveedor_id)
    if not db_proveedor:
        return None
    db.delete(db_proveedor)
    db.commit()
    return db_proveedor

# =========================
# 📌 CRUD CLIENTE
# =========================
# Crear cliente
def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Obtener todos
def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

# Obtener por ID
def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

# Actualizar (PUT/PATCH)
def update_cliente(db: Session, cliente_id: int, cliente: schemas.ClienteUpdate):
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None
    for key, value in cliente.model_dump(exclude_unset=True).items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Eliminar
def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id)
    if not db_cliente:
        return None
    db.delete(db_cliente)
    db.commit()
    return db_cliente

from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# =========================
# 📌 Crear Documento
# =========================
def create_documento(db: Session, documento: schemas.DocumentoCreate):
    db_documento = models.Documento(
        tipo=documento.tipo,
        numero=documento.numero,
        cliente_id=documento.cliente_id,
        proveedor_id=documento.proveedor_id,
        operacion=documento.operacion
    )
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)

    for det in documento.detalles:
        producto = db.query(models.Producto).filter(models.Producto.id == det.producto_id).first()
        if not producto:
            raise ValueError(f"Producto ID {det.producto_id} no existe")

        precio_unitario = producto.precio_venta if documento.operacion == "VENTA" else producto.precio_compra
        subtotal = det.cantidad * precio_unitario

        db_detalle = models.DetalleDocumento(
            documento_id=db_documento.id,
            producto_id=det.producto_id,
            cantidad=det.cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal
        )
        db.add(db_detalle)

        # Ajustar stock
        if documento.operacion == "VENTA":
            producto.stock_actual -= det.cantidad
            movimiento_tipo = "salida"
        else:
            producto.stock_actual += det.cantidad
            movimiento_tipo = "entrada"
        db.add(producto)

        db_movimiento = models.Movimiento(
            producto_id=det.producto_id,
            tipo=movimiento_tipo,
            cantidad=det.cantidad,
            fecha=datetime.utcnow()
        )
        db.add(db_movimiento)

    db.commit()
    db.refresh(db_documento)
    return db_documento


# =========================
# 📌 Listar todos los documentos
# =========================
def get_documentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Documento).offset(skip).limit(limit).all()


# =========================
# 📌 Obtener documento por ID
# =========================
def get_documento(db: Session, documento_id: int):
    return db.query(models.Documento).filter(models.Documento.id == documento_id).first()


# =========================
# 📌 Actualizar Documento (PUT)
# =========================
def update_documento(db: Session, documento_id: int, documento_update: schemas.DocumentoUpdateFull):
    db_documento = db.query(models.Documento).filter(models.Documento.id == documento_id).first()
    if not db_documento:
        return None

    # Revertir stock de detalles existentes
    detalles_existentes = db.query(models.DetalleDocumento).filter(models.DetalleDocumento.documento_id == documento_id).all()
    for det in detalles_existentes:
        producto = db.query(models.Producto).filter(models.Producto.id == det.producto_id).first()
        if producto:
            if db_documento.operacion == "VENTA":
                producto.stock_actual += det.cantidad
            else:
                producto.stock_actual -= det.cantidad
            db.add(producto)

    # Eliminar detalles antiguos
    db.query(models.DetalleDocumento).filter(models.DetalleDocumento.documento_id == documento_id).delete()

    # Actualizar cabecera
    db_documento.tipo = documento_update.tipo
    db_documento.numero = documento_update.numero
    db_documento.cliente_id = documento_update.cliente_id
    db_documento.proveedor_id = documento_update.proveedor_id
    db_documento.operacion = documento_update.operacion
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)

    # Insertar nuevos detalles y ajustar stock/movimientos
    for det in documento_update.detalles:
        producto = db.query(models.Producto).filter(models.Producto.id == det.producto_id).first()
        if not producto:
            raise ValueError(f"Producto ID {det.producto_id} no existe")

        precio_unitario = producto.precio_venta if documento_update.operacion == "VENTA" else producto.precio_compra
        subtotal = det.cantidad * precio_unitario

        db_detalle = models.DetalleDocumento(
            documento_id=db_documento.id,
            producto_id=det.producto_id,
            cantidad=det.cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal
        )
        db.add(db_detalle)

        if documento_update.operacion == "VENTA":
            producto.stock_actual -= det.cantidad
            movimiento_tipo = "salida"
        else:
            producto.stock_actual += det.cantidad
            movimiento_tipo = "entrada"
        db.add(producto)

        db_movimiento = models.Movimiento(
            producto_id=det.producto_id,
            tipo=movimiento_tipo,
            cantidad=det.cantidad,
            fecha=datetime.utcnow()
        )
        db.add(db_movimiento)

    db.commit()
    db.refresh(db_documento)
    return db_documento


# =========================
# 📌 Eliminar documento
# =========================
def delete_documento(db: Session, documento_id: int):
    documento = db.query(models.Documento).filter(models.Documento.id == documento_id).first()
    if not documento:
        return None

    db.delete(documento)
    db.commit()
    return documento
