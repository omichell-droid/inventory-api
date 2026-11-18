# test_app.py
# Tests for the CRUD routes in app.py

# ---------- GET ----------

def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_get_one_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Organic Almond Milk"


def test_get_item_that_does_not_exist(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


# ---------- POST ----------

def test_add_item(client):
    new_item = {"product_name": "Bread", "brands": "Bakery", "price": 2.5, "stock": 10}
    response = client.post("/inventory", json=new_item)

    assert response.status_code == 201
    assert response.get_json()["id"] == 4
    assert response.get_json()["product_name"] == "Bread"

    # The list should now have 4 items
    all_items = client.get("/inventory").get_json()
    assert len(all_items) == 4


def test_add_item_without_name(client):
    response = client.post("/inventory", json={"price": 2.5})
    assert response.status_code == 400


# ---------- PATCH ----------

def test_update_price_and_stock(client):
    response = client.patch("/inventory/2", json={"price": 7.99, "stock": 5})
    assert response.status_code == 200
    assert response.get_json()["price"] == 7.99
    assert response.get_json()["stock"] == 5


def test_update_does_not_change_id(client):
    response = client.patch("/inventory/2", json={"id": 50})
    assert response.get_json()["id"] == 2


def test_update_item_that_does_not_exist(client):
    response = client.patch("/inventory/999", json={"stock": 1})
    assert response.status_code == 404


# ---------- DELETE ----------

def test_delete_item(client):
    response = client.delete("/inventory/3")
    assert response.status_code == 200

    # The item should be gone now
    response = client.get("/inventory/3")
    assert response.status_code == 404


def test_delete_item_that_does_not_exist(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404
