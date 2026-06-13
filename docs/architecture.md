# Architecture - Coorp Capsule API

## Resumen

Coorp Capsule API usa una arquitectura modular simple para el MVP. La aplicacion expone endpoints HTTP con FastAPI, valida entradas con Pydantic, mantiene el estado temporal en memoria y usa Redis como cache para acelerar consultas repetidas de productos. Docker Compose levanta la API y Redis como servicios separados.

## Bloques principales

| Bloque | Responsabilidad |
|---|---|
| Cliente HTTP | Consume la API desde Swagger, curl, Postman u otra herramienta |
| FastAPI app | Publica endpoints, aplica reglas de negocio y retorna respuestas HTTP |
| Modelos Pydantic | Validan request bodies y definen respuestas |
| Servicio de inventario | Gestiona productos, estados y movimientos |
| Almacenamiento en memoria | Guarda productos y movimientos durante la ejecucion local |
| Redis | Guarda respuestas cacheadas de productos con TTL |
| Docker Compose | Orquesta el contenedor de la API y el contenedor de Redis |
| OpenAPI | Documenta contrato, requests, responses y errores |

## Diagrama Mermaid

```mermaid
flowchart LR
    user["Usuario / Cliente HTTP"] --> swagger["Swagger UI / Cliente REST"]
    swagger --> api["FastAPI - Coorp Capsule API"]
    api --> validators["Modelos Pydantic"]
    validators --> rules["Reglas de negocio"]
    rules --> memory["Almacenamiento en memoria"]
    api <--> redis["Redis cache"]
    api --> openapi["Contrato OpenAPI"]
```

## Flujo de cache Redis

```mermaid
sequenceDiagram
    actor U as Usuario
    participant API as FastAPI
    participant R as Redis
    participant M as Memoria

    U->>API: GET /products/{product_id}
    API->>R: GET coorp:product:{product_id}
    alt Cache hit
        R-->>API: Producto en JSON
        API-->>U: 200 X-Cache HIT
    else Cache miss
        R-->>API: Sin dato
        API->>M: Buscar producto
        M-->>API: Producto
        API->>R: SETEX coorp:product:{product_id} 60
        API-->>U: 200 X-Cache MISS
    end
```

## Flujo de movimiento de inventario

```mermaid
sequenceDiagram
    actor U as Usuario
    participant API as FastAPI
    participant V as Validacion
    participant M as Memoria

    U->>API: POST /movements
    API->>V: Validar producto_id, tipo, cantidad
    V-->>API: Datos validos
    API->>M: Buscar producto
    alt Producto no existe
        API-->>U: 404 Producto no encontrado
    else Producto inactivo
        API-->>U: 400 Producto inactivo
    else Salida sin stock
        API-->>U: 400 Stock insuficiente
    else Movimiento valido
        API->>M: Actualizar stock y guardar movimiento
        API-->>U: 201 Movimiento creado
    end
```

## Decision arquitectonica

### Decision

Usar FastAPI con almacenamiento temporal en memoria y Redis como cache-aside para consultas de producto.

### Justificacion

FastAPI permite construir una API funcional de forma rapida, validar entradas con Pydantic y generar documentacion interactiva en Swagger. Redis se agrega porque `GET /products/{product_id}` puede repetirse muchas veces en operaciones de inventario y es un buen candidato para cache. El TTL evita datos guardados indefinidamente y la API invalida la clave cuando cambia el producto o su stock.

### Consecuencia

La API es facil de ejecutar localmente con `docker compose up --build` y permite demostrar cache hit/cache miss. La limitacion principal es que los datos base siguen en memoria y se pierden al reiniciar el servidor. En una siguiente iteracion, el almacenamiento en memoria se reemplazaria por PostgreSQL o SQLite.

## Evolucion propuesta

- Agregar persistencia con base de datos.
- Separar rutas, modelos y servicios en modulos.
- Agregar autenticacion basica.
- Agregar pruebas automatizadas de reglas de negocio.
- Publicar tablero del backlog en GitHub Projects.
