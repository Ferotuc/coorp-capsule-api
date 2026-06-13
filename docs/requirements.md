# Requirements - Coorp Capsule API

## Objetivo del MVP

Construir una API ejecutable que represente el flujo principal de inventario para Coorp Capsule: productos y movimientos de stock.

## Requerimientos funcionales

| ID | Requerimiento | Prioridad |
|---|---|---|
| RF-01 | Crear productos con codigo, nombre, precio y estado activo | Must |
| RF-02 | Consultar un producto por identificador | Must |
| RF-03 | Listar productos registrados | Must |
| RF-04 | Actualizar nombre, precio y estado de un producto | Should |
| RF-05 | Cambiar estado activo/inactivo de un producto | Must |
| RF-06 | Registrar movimientos de entrada de stock | Must |
| RF-07 | Registrar movimientos de salida de stock | Must |
| RF-08 | Rechazar salidas cuando el stock es insuficiente | Must |
| RF-09 | Consultar movimientos por producto | Should |

## Requerimientos no funcionales

| ID | Requerimiento | Prioridad |
|---|---|---|
| RNF-01 | La API debe ejecutarse localmente con Uvicorn | Must |
| RNF-02 | El contrato debe estar documentado en OpenAPI | Must |
| RNF-03 | Los request bodies deben validarse con modelos Pydantic | Must |
| RNF-04 | La documentacion debe incluir arquitectura y diagrama Mermaid | Must |
| RNF-05 | El almacenamiento puede ser temporal en memoria para el MVP | Should |
| RNF-06 | El entorno local debe levantarse con Docker Compose | Must |
| RNF-07 | Redis debe ejecutarse en contenedor Docker | Must |
| RNF-08 | `GET /products/{product_id}` debe usar cache Redis con TTL | Must |

## Reglas de negocio

- El codigo de producto no puede repetirse.
- El precio debe ser mayor o igual a cero.
- La cantidad de un movimiento debe ser mayor que cero.
- Una salida no puede dejar stock negativo.
- No se registran movimientos sobre productos inactivos.
- Si el producto no existe, la API responde 404.
- Toda respuesta cacheada de producto debe expirar por TTL.
- Si un producto cambia o cambia su stock, la API invalida su clave de cache.

## Endpoints minimos implementados

- `POST /products`: operacion de creacion.
- `GET /products/{product_id}`: operacion de consulta con cache Redis.
- `PATCH /products/{product_id}/status`: cambio de estado.
- `POST /movements`: endpoint adicional del flujo principal.
- `GET /products/{product_id}/movements`: consulta del historial del flujo.

## Criterios de aceptacion principales

### Crear producto

Given que el usuario envia codigo, nombre y precio validos  
When llama `POST /products`  
Then la API crea el producto con stock inicial 0 y responde 201.

### Registrar salida

Given que existe un producto activo con stock disponible  
When el usuario llama `POST /movements` con tipo `salida` y cantidad valida  
Then la API registra el movimiento, descuenta el stock y responde 201.

### Stock insuficiente

Given que existe un producto con stock menor a la cantidad solicitada  
When el usuario registra una salida  
Then la API responde 400 con el mensaje `Stock insuficiente para realizar la salida`.

### Cache de producto

Given que existe un producto y Redis esta disponible  
When el usuario llama por primera vez `GET /products/{product_id}`  
Then la API responde `X-Cache: MISS` y guarda `coorp:product:{product_id}` con TTL de 60 segundos.

Given que la clave sigue vigente en Redis  
When el usuario repite `GET /products/{product_id}`  
Then la API responde `X-Cache: HIT` desde Redis.
