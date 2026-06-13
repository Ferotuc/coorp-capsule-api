from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_product_and_register_entry():
    response = client.post(
        "/products",
        json={"codigo": "CAP-T-001", "nombre": "Capsula Test", "precio": 99.99, "activo": True},
    )

    assert response.status_code == 201
    product = response.json()
    assert product["stock"] == 0

    movement_response = client.post(
        "/movements",
        json={
            "producto_id": product["id"],
            "tipo": "entrada",
            "cantidad": 5,
            "descripcion": "Ingreso de prueba",
        },
    )

    assert movement_response.status_code == 201

    product_response = client.get(f"/products/{product['id']}")
    assert product_response.json()["stock"] == 5


def test_reject_output_when_stock_is_insufficient():
    product_response = client.post(
        "/products",
        json={"codigo": "CAP-T-002", "nombre": "Capsula Sin Stock", "precio": 50.0, "activo": True},
    )
    product = product_response.json()

    response = client.post(
        "/movements",
        json={
            "producto_id": product["id"],
            "tipo": "salida",
            "cantidad": 1,
            "descripcion": "Salida no valida",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Stock insuficiente para realizar la salida"


def test_product_not_found_returns_404():
    response = client.get("/products/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Producto no encontrado"
