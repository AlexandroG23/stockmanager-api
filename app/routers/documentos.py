from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from fastapi.responses import Response
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"],
)

# =========================
# 📌 Crear Documento
# =========================
@router.post("/", response_model=schemas.Documento, status_code=status.HTTP_201_CREATED)
def create_documento(documento: schemas.DocumentoCreate, db: Session = Depends(get_db)):
    return crud.create_documento(db=db, documento=documento)

# =========================
# 📌 Listar Documentos
# =========================
@router.get("/", response_model=list[schemas.Documento])
def read_documentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_documentos(db, skip=skip, limit=limit)

# =========================
# 📌 Obtener Documento por ID
# =========================
@router.get("/{documento_id}", response_model=schemas.Documento)
def read_documento(documento_id: int, db: Session = Depends(get_db)):
    db_documento = crud.get_documento(db, documento_id)
    if not db_documento:
        raise HTTPException(status_code=404, detail=f"Documento {documento_id} no encontrado")
    return db_documento

# =========================
# 📌 Actualizar Documento (PUT)
# =========================
@router.put("/{documento_id}", response_model=schemas.Documento)
def update_documento(documento_id: int, documento_update: schemas.DocumentoCreate, db: Session = Depends(get_db)):
    db_documento = crud.update_documento(db, documento_id=documento_id, documento_update=documento_update)
    if not db_documento:
        raise HTTPException(status_code=404, detail=f"Documento {documento_id} no encontrado")
    return db_documento

# =========================
# 📌 Eliminar Documento
# =========================
@router.delete("/{documento_id}", status_code=status.HTTP_200_OK)
def delete_documento(documento_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_documento(db, documento_id=documento_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Documento {documento_id} no encontrado")
    return {"message": f"Documento {documento_id} eliminado correctamente"}


# =========================
# 📌 Generar PDF
# =========================
@router.get("/{documento_id}/pdf")
def generar_pdf(documento_id: int, db: Session = Depends(get_db)):
    db_documento = crud.get_documento(db, documento_id)
    if not db_documento:
        raise HTTPException(status_code=404, detail=f"Documento {documento_id} no encontrado")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # 🔑 Metadatos
    doc.title = f"{db_documento.tipo} {db_documento.numero}"
    doc.author = "Mi Sistema de Facturación"
    doc.subject = f"Documento {db_documento.tipo}"
    doc.keywords = "Factura, Boleta, Documento, Reporte"

    styles = getSampleStyleSheet()
    estilos = {
        "titulo": styles["Title"],
        "normal": styles["Normal"],
        "negrita": styles["Heading3"],
    }

    elementos = []

    # =========================
    # Encabezado
    # =========================
    elementos.append(Paragraph("<b>SISTEMA DE FACTURACIÓN</b>", estilos["titulo"]))
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph(f"<b>{db_documento.tipo} {db_documento.numero}</b>", estilos["negrita"]))
    elementos.append(Paragraph(f"Operación: {db_documento.operacion}", estilos["normal"]))
    elementos.append(Spacer(1, 12))

    # =========================
    # Datos de Cliente y Proveedor
    # =========================
    data_info = []
    if db_documento.cliente:
        data_info.append(["Cliente:", db_documento.cliente.nombre])
    if db_documento.proveedor:
        data_info.append(["Proveedor:", db_documento.proveedor.nombre])

    if data_info:
        tabla_info = Table(data_info, colWidths=[100, 400])
        tabla_info.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elementos.append(tabla_info)
        elementos.append(Spacer(1, 12))

    # =========================
    # Tabla de Detalles
    # =========================
    data = [["Producto", "Cantidad", "Precio", "Subtotal"]]
    total = 0
    for det in db_documento.detalles:
        precio = det.producto.precio_venta if db_documento.operacion == "VENTA" else det.producto.precio_compra
        subtotal = det.cantidad * precio
        total += subtotal
        data.append([det.producto.nombre, det.cantidad, f"S/ {precio:.2f}", f"S/ {subtotal:.2f}"])
    data.append(["", "", "TOTAL", f"S/ {total:.2f}"])

    tabla = Table(data, colWidths=[200, 80, 100, 100])
    tabla.setStyle(TableStyle([
        # Cabecera
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

        # Celdas
        ("GRID", (0, 0), (-1, -2), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),

        # Totales
        ("BACKGROUND", (-2, -1), (-1, -1), colors.lightgrey),
        ("TEXTCOLOR", (-2, -1), (-1, -1), colors.black),
        ("FONTSIZE", (-2, -1), (-1, -1), 11),
        ("ALIGN", (-2, -1), (-1, -1), "RIGHT"),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 20))

    # =========================
    # Pie de página
    # =========================
    elementos.append(Paragraph("Gracias por su preferencia 🙌", estilos["normal"]))

    doc.build(elementos)
    pdf = buffer.getvalue()
    buffer.close()

    # Descargar con nombre
    filename = f"{db_documento.tipo}_{db_documento.numero}.pdf"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}

    return Response(content=pdf, media_type="application/pdf", headers=headers)