# Coorp Capsule API

Coorp Capsule API es un MVP tecnico para gestionar inventario basico de productos y registrar movimientos de entrada o salida de stock. El flujo principal implementado permite crear productos, consultar su informacion, cambiar su estado y registrar movimientos que actualizan existencias.

## Stack

- Python 3.11+
- FastAPI
- Pydantic
- Uvicorn
- Redis como cache
- Docker Compose
- Almacenamiento temporal en memoria

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

Luego abrir:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Redis: `localhost:6379`

## Ejecutar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Luego abrir:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI generado por FastAPI: http://127.0.0.1:8000/openapi.json

## Endpoints del MVP

| Metodo | Endpoint | Proposito |
|---|---|---|
| GET | `/health` | Verificar que la API esta activa |
| POST | `/products` | Crear un producto |
| GET | `/products` | Listar productos |
| GET | `/products/{product_id}` | Consultar un producto con cache Redis |
| PUT | `/products/{product_id}` | Actualizar datos del producto |
| PATCH | `/products/{product_id}/status` | Activar o desactivar un producto |
| POST | `/movements` | Registrar entrada o salida de stock |
| GET | `/products/{product_id}/movements` | Consultar movimientos de un producto |

## Ejemplo rapido

Crear producto:

```bash
curl -X POST http://127.0.0.1:8000/products ^
  -H "Content-Type: application/json" ^
  -d "{\"codigo\":\"CAP-001\",\"nombre\":\"Capsula Ejecutiva\",\"precio\":125.50,\"activo\":true}"
```

Registrar entrada:

```bash
curl -X POST http://127.0.0.1:8000/movements ^
  -H "Content-Type: application/json" ^
  -d "{\"producto_id\":1,\"tipo\":\"entrada\",\"cantidad\":10,\"descripcion\":\"Ingreso inicial\"}"
```

Consultar producto:

```bash
curl http://127.0.0.1:8000/products/1
```

Demostrar cache:

```bash
curl -i http://127.0.0.1:8000/products/1
curl -i http://127.0.0.1:8000/products/1
```

La primera respuesta devuelve `X-Cache: MISS` y guarda la clave `coorp:product:1` en Redis por 60 segundos. La segunda respuesta devuelve `X-Cache: HIT`.

## Documentacion

- [Resumen del sistema](docs/system-brief.md)
- [Requerimientos](docs/requirements.md)
- [Arquitectura](docs/architecture.md)
- [Cache Redis](docs/cache.md)
- [Contrato OpenAPI](docs/api/openapi.yaml)
- [Backlog del MVP](docs/backlog-mvp.md)
- [Fuente para PDF de entrega](docs/submission-pdf.md)

## Repositorio

Repositorio publico: https://github.com/Ferotuc/coorp-capsule-api
