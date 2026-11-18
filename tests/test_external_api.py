# test_external_api.py
# Tests for the OpenFoodFacts code.
# We use "mock" to fake the internet, so the tests don't need a connection.

from unittest.mock import Mock, patch

from external_api import get_product_by_barcode, search_products_by_name

FAKE_API_ANSWER = {
    "status": 1,
    "product": {
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds"
    }
}


# ---------- external_api.py functions ----------

@patch("external_api.requests.get")
def test_get_product_by_barcode_found(fake_get):
    fake_response = Mock()
    fake_response.json.return_value = FAKE_API_ANSWER
    fake_get.return_value = fake_response

    product = get_product_by_barcode("12345")

    assert product["product_name"] == "Organic Almond Milk"
    assert product["brands"] == "Silk"


@patch("external_api.requests.get")
def test_get_product_by_barcode_not_found(fake_get):
    fake_response = Mock()
    fake_response.json.return_value = {"status": 0}
    fake_get.return_value = fake_response

    assert get_product_by_barcode("00000") is None


@patch("external_api.requests.get")
def test_get_product_when_internet_is_down(fake_get):
    fake_get.side_effect = Exception("No internet")
    assert get_product_by_barcode("12345") is None


@patch("external_api.requests.get")
def test_search_products_by_name(fake_get):
    fake_response = Mock()
    fake_response.json.return_value = {
        "products": [{"code": "111", "product_name": "Almond Milk", "brands": "Silk"}]
    }
    fake_get.return_value = fake_response

    results = search_products_by_name("almond")

    assert len(results) == 1
    assert results[0]["barcode"] == "111"


# ---------- the Flask helper routes ----------

@patch("app.get_product_by_barcode")
def test_search_route_with_barcode(fake_lookup, client):
    fake_lookup.return_value = {"product_name": "Nutella", "brands": "Ferrero"}
    response = client.get("/external/search?barcode=3017620422003")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Nutella"


@patch("app.search_products_by_name")
def test_search_route_with_name(fake_search, client):
    fake_search.return_value = [{"product_name": "Milk"}]
    response = client.get("/external/search?name=milk")
    assert response.status_code == 200


def test_search_route_with_nothing(client):
    response = client.get("/external/search")
    assert response.status_code == 400


@patch("app.get_product_by_barcode")
def test_import_adds_product_to_inventory(fake_lookup, client):
    fake_lookup.return_value = {
        "barcode": "12345",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds"
    }
    response = client.post("/inventory/import", json={"barcode": "12345", "price": 3.5, "stock": 12})

    assert response.status_code == 201
    assert response.get_json()["id"] == 4
    assert len(client.get("/inventory").get_json()) == 4


@patch("app.get_product_by_barcode")
def test_import_unknown_barcode(fake_lookup, client):
    fake_lookup.return_value = None
    response = client.post("/inventory/import", json={"barcode": "00000"})
    assert response.status_code == 404
