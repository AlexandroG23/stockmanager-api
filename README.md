# API de Gestión de Inventario

API para gestionar **productos**, **categorías**, **proveedores**, **clientes**, **documentos** y **movimientos de inventario**.

Esta API está construida con **FastAPI** y expone documentación automática en Swagger y ReDoc.

## 🚀 URLs de documentación

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## ⚡ Base URL
> **Nota:** El **backend** se ejecutará por defecto en `http://127.0.0.1:8000/`

## 🛠️ Tecnologías y Herramientas

- **Python**: Lenguaje principal
- **FastAPI**: Framework para construir la API
- **SQLAlchemy**: ORM para la base de datos
- **Pydantic**: Validación de datos y esquemas
- **Uvicorn**: Servidor ASGI
- **Base de datos**: SQLite / PostgreSQL / MySQL (según configuración)
- **Datetime / Timezone Handling**: Manejo de fechas y horas
- **APIRouter de FastAPI**: Organización modular de rutas
- **Depends de FastAPI**: Inyección de dependencias (sesión DB)

## 📦 Endpoints

### Productos

| Método | Endpoint           | Descripción                        |
|--------|--------------------|------------------------------------|
| GET    | `/productos/`      | Lista todos los productos          |
| GET    | `/productos/{id}`  | Obtiene un producto por ID         |
| POST   | `/productos/`      | Crea un producto                   |
| PUT    | `/productos/{id}`  | Actualiza un producto completo     |
| PATCH  | `/productos/{id}`  | Actualiza parcialmente un producto |
| DELETE | `/productos/{id}`  | Elimina un producto                |

### Categorías

| Método | Endpoint           | Descripción                           |
|--------|--------------------|---------------------------------------|
| GET    | `/categorias/`     | Lista todas las categorías            |
| GET    | `/categorias/{id}` | Obtiene una categoría por ID          |
| POST   | `/categorias/`     | Crea una nueva categoría              |
| PUT    | `/categorias/{id}` | Actualiza completamente una categoría |
| PATCH  | `/categorias/{id}` | Actualiza parcialmente una categoría  |
| DELETE | `/categorias/{id}` | Elimina una categoría                 |

### Proveedores

| Método | Endpoint             | Descripción                           |
|--------|----------------------|---------------------------------------|
| GET    | `/proveedores/`      | Lista todos los proveedores           |
| GET    | `/proveedores/{id}`  | Obtiene un proveedor por ID           |
| POST   | `/proveedores/`      | Crea un nuevo proveedor               |
| PUT    | `/proveedores/{id}`  | Actualiza completamente un proveedor  |
| PATCH  | `/proveedores/{id}`  | Actualiza parcialmente un proveedor   |
| DELETE | `/proveedores/{id}`  | Elimina un proveedor                  |

### Clientes

| Método | Endpoint           | Descripción                        |
|--------|--------------------|------------------------------------|
| GET    | `/clientes/`       | Lista todos los clientes           |
| GET    | `/clientes/{id}`   | Obtiene un cliente por ID          |
| POST   | `/clientes/`       | Crea un nuevo cliente              |
| PUT    | `/clientes/{id}`   | Actualiza completamente un cliente |
| PATCH  | `/clientes/{id}`   | Actualiza parcialmente un cliente  |
| DELETE | `/clientes/{id}`   | Elimina un cliente                 |

### Documentos

| Método | Endpoint                 | Descripción                                       |
|--------|--------------------------|---------------------------------------------------|
| GET    | `/documentos/`           | Lista todos los documentos                        |
| GET    | `/documentos/{id}`       | Obtiene un documento por ID                       |
| POST   | `/documentos/`           | Crea un nuevo documento con detalles              |
| PUT    | `/documentos/{id}`       | Actualiza completamente un documento              |
| PATCH  | `/documentos/{id}`       | Actualiza parcialmente un documento               |
| DELETE | `/documentos/{id}`       | Elimina un documento                              |

### Movimientos

| Método | Endpoint                     | Descripción                                     |
|--------|------------------------------|-------------------------------------------------|
| GET    | `/movimientos/`              | Lista todos los movimientos                     |
| GET    | `/movimientos/{id}`          | Obtiene un movimiento por ID                    |
| GET    | `/movimientos/producto/{id}` | Lista movimientos de un producto específico     |
| GET    | `/movimientos/reportes`      | Filtra movimientos por tipo y rango de fechas   |
| POST   | `/movimientos/`              | Crea un nuevo movimiento manual                 |

