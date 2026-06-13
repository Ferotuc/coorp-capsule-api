# Backlog MVP - Coorp Capsule API

Este archivo sirve como base para cargar las historias en una herramienta web como GitHub Projects, Trello, Jira o ClickUp. Para la entrega final, el tablero debe existir en una herramienta real con columnas `To Do`, `In Progress` y `Done`.

## Historias

| ID | Historia | Prioridad | Estado sugerido |
|---|---|---|---|
| US-01 | Como encargado quiero crear productos para iniciar el inventario | Must | Done |
| US-02 | Como encargado quiero consultar un producto por ID para revisar su informacion | Must | Done |
| US-03 | Como encargado quiero listar productos para ver el inventario disponible | Must | Done |
| US-04 | Como encargado quiero registrar entradas de stock para actualizar existencias | Must | Done |
| US-05 | Como encargado quiero registrar salidas de stock para reflejar entregas | Must | Done |
| US-06 | Como administrador quiero bloquear salidas sin stock suficiente para evitar inventario negativo | Must | Done |
| US-07 | Como administrador quiero cambiar el estado de un producto para impedir movimientos sobre productos inactivos | Should | Done |
| US-08 | Como encargado quiero consultar movimientos por producto para tener trazabilidad | Should | Done |
| US-09 | Como administrador quiero autenticacion para proteger la API | Could | To Do |
| US-10 | Como administrador quiero reportes de inventario para analizar movimientos | Could | To Do |
| US-11 | Como operador quiero multiples bodegas para separar inventarios por ubicacion | Won't | To Do |

## Criterios Given / When / Then

### US-01 - Crear productos

Given que el encargado tiene un codigo, nombre y precio validos  
When envia una solicitud `POST /products`  
Then la API registra el producto, asigna un ID, inicia el stock en 0 y responde 201.

### US-05 - Registrar salidas de stock

Given que existe un producto activo con stock disponible  
When el encargado envia una solicitud `POST /movements` con tipo `salida`  
Then la API registra el movimiento, descuenta el stock y responde 201.

### US-06 - Evitar inventario negativo

Given que existe un producto con stock menor a la cantidad solicitada  
When el encargado intenta registrar una salida  
Then la API rechaza la operacion con 400 y no modifica el stock.

## Tablero recomendado

- To Do: US-09, US-10, US-11.
- In Progress: tareas de video, PDF y carga del tablero web.
- Done: US-01 a US-08.
