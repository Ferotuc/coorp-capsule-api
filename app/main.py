from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

app = FastAPI(
    title="Coorp Capsule API",
    description="API MVP para gestión de inventario y movimientos de productos.",
    version="1.0.0"
)

class ProductCreate(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=30, description="Código único del producto")
    nombre: str = Field(..., min_length=1, max_length=120, description="Nombre del producto")
    precio: float = Field(..., ge=0, description="Precio del producto")
    activo: bool = True

class ProductUpdate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=120)
    precio: float = Field(..., ge=0)
    activo: bool

class ProductResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    precio: float
    activo: bool
    stock: int

class MovementCreate(BaseModel):
    producto_id: int
    tipo: Literal["entrada", "salida"]
    cantidad: int = Field(..., gt=0, description="Cantidad mayor que 0")
    descripcion: str = Field(..., min_length=1, max_length=200)

class MovementResponse(BaseModel):
    id: int
    producto_id: int
    tipo: str
    cantidad: int
    descripcion: str
    fecha: str

products = []
movements = []

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

@app.post("/products", response_model=ProductResponse, status_code=201)
def crear_producto(producto: ProductCreate):
    global product_id_counter

    if existe_codigo(producto.codigo):
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese código")

    nuevo_producto = {
        "id": product_id_counter,
        "codigo": producto.codigo,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "activo": producto.activo,
        "stock": 0
    }

    products.append(nuevo_producto)
    product_id_counter += 1
    return nuevo_producto

@app.get("/products", response_model=List[ProductResponse])
def listar_productos():
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def obtener_producto(product_id: int):
    producto = buscar_producto(product_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/products/{product_id}", response_model=ProductResponse)
def actualizar_producto(product_id: int, datos: ProductUpdate):
    producto = buscar_producto(product_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto["nombre"] = datos.nombre
    producto["precio"] = datos.precio
    producto["activo"] = datos.activo

    return producto

@app.post("/movements", response_model=MovementResponse, status_code=201)
def registrar_movimiento(movimiento: MovementCreate):
    global movement_id_counter

    producto = buscar_producto(movimiento.producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if movimiento.tipo == "salida" and producto["stock"] < movimiento.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente para realizar la salida")

    if movimiento.tipo == "entrada":
        producto["stock"] += movimiento.cantidad
    elif movimiento.tipo == "salida":
        producto["stock"] -= movimiento.cantidad

    nuevo_movimiento = {
        "id": movement_id_counter,
        "producto_id": movimiento.producto_id,
        "tipo": movimiento.tipo,
        "cantidad": movimiento.cantidad,
        "descripcion": movimiento.descripcion,
        "fecha": datetime.now().isoformat()
    }

    movements.append(nuevo_movimiento)
    movement_id_counter += 1
    return nuevo_movimiento

@app.get("/products/{product_id}/movements", response_model=List[MovementResponse])
def listar_movimientos_producto(product_id: int):
    producto = buscar_producto(product_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    resultado = [m for m in movements if m["producto_id"] == product_id]
    return resultado