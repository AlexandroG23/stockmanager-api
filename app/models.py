from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base

# =========================
# 📌 Categoria
# =========================
class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    descripcion = Column(String, nullable=True)

    # Relación con productos
    productos = relationship("Producto", back_populates="categoria")


# =========================
# 📌 Producto
# =========================
class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String, unique=True, index=True, nullable=True)
    nombre = Column(String, index=True, nullable=False)
    precio_compra = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=0)
    unidad_medida = Column(String, nullable=False, default="unidad")

    # Relaciones
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    categoria = relationship("Categoria", back_populates="productos")
    movimientos = relationship("Movimiento", back_populates="producto")


# =========================
# 📌 Proveedor
# =========================
class Proveedor(Base):
    __tablename__ = 'proveedores'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    ruc = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=True)
    direccion = Column(String, nullable=True)
    email = Column(String, nullable=True)

    documentos = relationship("Documento", back_populates="proveedor")


# =========================
# 📌 Cliente
# =========================
class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    documento = Column(String, unique=True, index=True)  # DNI, RUC, etc.
    direccion = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)

    documentos = relationship("Documento", back_populates="cliente")


# =========================
# 📌 Documento
# =========================
class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)           # Boleta, Factura, etc.
    operacion = Column(String, nullable=False)      # "COMPRA" o "VENTA"
    numero = Column(String, unique=True, index=True, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)

    # Relaciones
    cliente = relationship("Cliente", back_populates="documentos")
    proveedor = relationship("Proveedor", back_populates="documentos")
    detalles = relationship("DetalleDocumento", back_populates="documento", cascade="all, delete-orphan")


# =========================
# 📌 DetalleDocumento
# =========================
class DetalleDocumento(Base):
    __tablename__ = "detalle_documentos"

    id = Column(Integer, primary_key=True, index=True)
    documento_id = Column(Integer, ForeignKey("documentos.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relaciones
    documento = relationship("Documento", back_populates="detalles")
    producto = relationship("Producto")


# =========================
# 📌 Movimiento
# =========================
class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo = Column(String, nullable=False)          # "entrada" o "salida"
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    producto = relationship("Producto", back_populates="movimientos")