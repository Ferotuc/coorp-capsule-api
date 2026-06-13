from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator


app = FastAPI(
    title="Coorp Capsule API",
    description="MVP tecnico para gestionar productos, stock y movimientos de inventario.",
    version="1.0.0",
)


class ProductCreate(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=30, description="Codigo unico del producto")
    nombre: str = Field(..., min_length=1, max_length=120, description="Nombre del producto")
    precio: float = Field(..., ge=0, description="Precio unitario del producto")
    activo: bool = True

    @field_validator("codigo", "nombre")
    @classmethod
    def trim_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El valor no puede estar vacio")
        return value


class ProductUpdate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=120)
    precio: float = Field(..., ge=0)
    activo: bool

    @field_validator("nombre")
    @classmethod
    def trim_nombre(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre no puede estar vacio")
        return value


class ProductStatusUpdate(BaseModel):
    activo: bool = Field(..., description="Estado operativo del producto")


class ProductResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    precio: float
    activo: bool
    stock: int


class MovementCreate(BaseModel):
    producto_id: int = Field(..., gt=0)
    tipo: Literal["entrada", "salida"]
    cantidad: int = Field(..., gt=0, description="Cantidad mayor que 0")
    descripcion: str = Field(..., min_length=1, max_length=200)

    @field_validator("descripcion")
    @classmethod
    def trim_descripcion(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("La descripcion no puede estar vacia")
        return value


class MovementResponse(BaseModel):
    id: int
    producto_id: int
    tipo: Literal["entrada", "salida"]
    cantidad: int
    descripcion: str
    fecha: str


products: list[dict] = []
movements: list[dict] = []
product_id_counter = 1
movement_id_counter = 1


def buscar_producto(product_id: int):
    for producto in products:
        if producto["id"] == product_id:
            return producto
    return None


def existe_codigo(codigo: str):
    for producto in products:
        if producto["codigo"].lower() == codigo.lower():
            return True
    return False


@app.get("/")
def root():
    return {"message": "Coorp Capsule API funcionando correctamente"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "coorp-capsule-api"}


@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductCreate):
    global product_id_counter

    if existe_codigo(producto.codigo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un producto con ese codigo",
        )

    nuevo_producto = {
        "id": product_id_counter,
        "codigo": producto.codigo,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "activo": producto.activo,
        "stock": 0,
    }

    products.append(nuevo_producto)
    product_id_counter += 1
    return nuevo_producto


@app.get("/products", response_model=list[ProductResponse])
def listar_productos():
    return products


@app.get("/products/{product_id}", response_model=ProductResponse)
def obtener_producto(product_id: int):
    producto = buscar_producto(product_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto


@app.put("/products/{product_id}", response_model=ProductResponse)
def actualizar_producto(product_id: int, datos: ProductUpdate):
    producto = buscar_producto(product_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    producto["nombre"] = datos.nombre
    producto["precio"] = datos.precio
    producto["activo"] = datos.activo

    return producto


@app.patch("/products/{product_id}/status", response_model=ProductResponse)
def cambiar_estado_producto(product_id: int, datos: ProductStatusUpdate):
    producto = buscar_producto(product_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    producto["activo"] = datos.activo
    return producto


@app.post("/movements", response_model=MovementResponse, status_code=status.HTTP_201_CREATED)
def registrar_movimiento(movimiento: MovementCreate):
    global movement_id_counter

    producto = buscar_producto(movimiento.producto_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    if not producto["activo"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden registrar movimientos en productos inactivos",
        )

    if movimiento.tipo == "salida" and producto["stock"] < movimiento.cantidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock insuficiente para realizar la salida",
        )

    if movimiento.tipo == "entrada":
        producto["stock"] += movimiento.cantidad
    else:
        producto["stock"] -= movimiento.cantidad

    nuevo_movimiento = {
        "id": movement_id_counter,
        "producto_id": movimiento.producto_id,
        "tipo": movimiento.tipo,
        "cantidad": movimiento.cantidad,
        "descripcion": movimiento.descripcion,
        "fecha": datetime.now(timezone.utc).isoformat(),
    }

    movements.append(nuevo_movimiento)
    movement_id_counter += 1
    return nuevo_movimiento


@app.get("/products/{product_id}/movements", response_model=list[MovementResponse])
def listar_movimientos_producto(product_id: int):
    producto = buscar_producto(product_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    return [movimiento for movimiento in movements if movimiento["producto_id"] == product_id]
