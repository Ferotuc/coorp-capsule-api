# System Brief - Coorp Capsule API

## Nombre del sistema

Coorp Capsule API.

## Problema que resuelve

Pequenas operaciones de inventario suelen registrar productos y movimientos en hojas de calculo, mensajes o documentos sueltos. Esto provoca errores de stock, falta de trazabilidad y poca claridad sobre que entradas o salidas afectaron cada producto.

Coorp Capsule API centraliza el flujo minimo de inventario: registrar productos, consultar su estado, activar o desactivar productos y registrar movimientos que actualizan el stock.

## Usuarios principales

- Encargado de inventario.
- Administrador operativo.
- Personal que registra entradas y salidas de productos.

## Flujo principal del MVP

1. El usuario crea un producto con codigo, nombre y precio.
2. El usuario consulta el producto registrado.
3. El usuario registra una entrada o salida de inventario.
4. La API valida que el producto exista, este activo y tenga stock suficiente para salidas.
5. La API actualiza el stock y guarda el movimiento.
6. El usuario consulta el historial de movimientos del producto.

## Scope

- Crear productos.
- Consultar productos.
- Actualizar datos del producto.
- Activar o desactivar productos.
- Registrar movimientos de entrada y salida.
- Consultar movimientos por producto.
- Validacion basica de datos.
- Errores documentados 400 y 404.

## No-scope

- Autenticacion real.
- Base de datos persistente.
- Reportes avanzados.
- Integracion con sistemas externos.
- Manejo de multiples bodegas.
- Interfaz web.

## Repositorio

https://github.com/Ferotuc/coorp-capsule-api
