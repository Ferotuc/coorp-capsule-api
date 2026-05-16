from fastapi import FastAPI
import redis
import json
import time

app = FastAPI()

# conexión a Redis
r = redis.Redis(host="redis", port=6379, decode_responses=True)

# base de datos falsa
fake_db = {
    "1": {"producto": "Laptop", "precio": 5000},
    "2": {"producto": "Mouse", "precio": 150},
    "3": {"producto": "Teclado", "precio": 300}
}

@app.get("/")
def home():
    return {"message": "API funcionando"}

@app.get("/inventory/{product_id}")
def get_product(product_id: str):
    
    cache_key = f"product:{product_id}"

    # Buscar en cache
    cached = r.get(cache_key)

    if cached:
        return {
            "source": "cache",
            "data": json.loads(cached)
        }

    # Simular base de datos lenta
    time.sleep(3)

    product = fake_db.get(product_id)

    if not product:
        return {"error": "Producto no encontrado"}

    # Guardar en Redis con TTL
    r.setex(cache_key, 60, json.dumps(product))

    return {
        "source": "database",
        "data": product
    }