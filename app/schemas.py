from pydantic import BaseModel, EmailStr, validator, field_validator
from typing import Optional, List

# =========================
# 📌 Categoria
# =========================
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdateFull(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# 📌 Producto
# =========================
class ProductoBase(BaseModel):
    codigo_barras: Optional[str] = None
    nombre: str
    precio_compra: float
    precio_venta: float
    stock_actual: int
    stock_minimo: int
    unidad_medida: str
    categoria_id: int

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdateFull(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    codigo_barras: Optional[str] = None
    nombre: Optional[str] = None
    precio_compra: Optional[float] = None
    precio_venta: Optional[float] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None
    unidad_medida: Optional[str] = None
    categoria_id: Optional[int] = None

class Producto(ProductoBase):
    id: int
    categoria: Optional[Categoria] = None

    class Config:
        from_attributes = True


# =========================
# 📌 Proveedor
# =========================
class ProveedorBase(BaseModel):
    nombre: str
    ruc: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    email: Optional[EmailStr] = None

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdateFull(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

class Proveedor(ProveedorBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# 📌 Cliente
# =========================
class ClienteBase(BaseModel):
    nombre: str
    documento: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdateFull(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    documento: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None

class Cliente(ClienteBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# 📌 Documento Detalle
# =========================
class DocumentoDetalleBase(BaseModel):
    producto_id: int
    cantidad: int

class DocumentoDetalleCreate(DocumentoDetalleBase):
    pass

class DocumentoDetalle(DocumentoDetalleBase):
    id: int
    subtotal: float  # Calculado automáticamente

    class Config:
        from_attributes = True


# =========================
# 📌 Documento
# =========================
class DocumentoBase(BaseModel):
    tipo: str
    numero: str
    cliente_id: Optional[int] = None
    proveedor_id: Optional[int] = None

class DocumentoCreate(DocumentoBase):
    operacion: str  # "COMPRA" o "VENTA"
    detalles: List[DocumentoDetalleCreate]

    @validator('operacion')
    def operacion_valida(cls, v):
        if v.upper() not in ["COMPRA", "VENTA"]:
            raise ValueError("operacion debe ser 'COMPRA' o 'VENTA'")
        return v.upper()

class DocumentoUpdateFull(DocumentoBase):
    operacion: str
    detalles: List[DocumentoDetalleCreate]

    @validator('operacion')
    def operacion_valida(cls, v):
        if v.upper() not in ["COMPRA", "VENTA"]:
            raise ValueError("operacion debe ser 'COMPRA' o 'VENTA'")
        return v.upper()

# PATCH opcional solo cabecera
class DocumentoUpdate(BaseModel):
    tipo: Optional[str] = None
    numero: Optional[str] = None
    cliente_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    operacion: Optional[str] = None

    @field_validator('operacion')
    def operacion_valida(cls, v):
        if v is not None and v.upper() not in ["COMPRA", "VENTA"]:
            raise ValueError("operacion debe ser 'COMPRA' o 'VENTA'")
        return v.upper() if v else v

class Documento(DocumentoBase):
    id: int
    operacion: str
    detalles: List[DocumentoDetalle] = []

    class Config:
        from_attributes = True

# =========================
# 📌 Movimiento
# =========================
from datetime import datetime

class MovimientoBase(BaseModel):
    producto_id: int
    tipo: str  # "entrada" o "salida"
    cantidad: int

class MovimientoCreate(MovimientoBase):
    pass

class Movimiento(MovimientoBase):
    id: int
    fecha: datetime
    producto: Optional[Producto]  # 👈 Esto incluye el producto completo

    class Config:
        from_attributes = True
