# Cache Redis - Coorp Capsule API

## Endpoint con cache

El endpoint cacheado es:

- `GET /products/{product_id}`

Se eligio este endpoint porque la consulta individual de producto es una lectura repetida y frecuente en un sistema de inventario. El dato puede consultarse varias veces desde Swagger, Postman, un frontend o una integracion antes de que el producto cambie.

## Claves generadas en Redis

La API genera una clave por producto:

```text
coorp:product:{product_id}
```

Ejemplo:

```text
coorp:product:1
```

El valor guardado es el producto serializado como JSON:

```json
{
  "id": 1,
  "codigo": "CAP-001",
  "nombre": "Capsula Ejecutiva",
  "precio": 125.5,
  "activo": true,
  "stock": 10
}
```

## TTL

El TTL definido es de 60 segundos.

La variable `CACHE_TTL_SECONDS` permite ajustar este valor. En `docker-compose.yml` se configura:

```yaml
CACHE_TTL_SECONDS: 60
```

## Estrategia

La estrategia usada es cache-aside:

1. La API recibe `GET /products/{product_id}`.
2. La API busca `coorp:product:{product_id}` en Redis.
3. Si existe, responde desde Redis.
4. Si no existe, consulta la fuente principal en memoria.
5. Si el producto existe, guarda el JSON en Redis con `SETEX` y TTL de 60 segundos.
6. La API responde al cliente.

## Cache hit

Cuando Redis ya tiene la clave vigente:

- La API responde con el producto desde Redis.
- La respuesta incluye `X-Cache: HIT`.
- No se consulta la lista principal en memoria.

## Cache miss

Cuando Redis no tiene la clave:

- La API consulta el producto en la fuente principal en memoria.
- Si existe, lo guarda en Redis con TTL usando `SETEX`.
- La respuesta incluye `X-Cache: MISS`.

Si Redis no esta disponible en ejecucion local sin Docker, la API sigue funcionando y responde con `X-Cache: BYPASS`.

## Invalidacion

La API elimina la clave `coorp:product:{product_id}` cuando:

- Se actualiza el producto con `PUT /products/{product_id}`.
- Se cambia su estado con `PATCH /products/{product_id}/status`.
- Se registra un movimiento con `POST /movements` y cambia el stock.

## Riesgos y limitaciones

- La fuente principal del MVP sigue en memoria, por lo que los datos se pierden al reiniciar la API.
- El TTL corto reduce el riesgo de dato viejo, pero no reemplaza una base de datos persistente.
- Si Redis no esta disponible, la API no falla; simplemente omite el cache.
- En una version productiva se agregaria monitoreo de Redis y persistencia en PostgreSQL.
