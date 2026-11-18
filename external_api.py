# external_api.py
# Functions that get product information from the OpenFoodFacts API.

import requests

BASE_URL = "https://world.openfoodfacts.org"

# OpenFoodFacts asks apps to say who they are
HEADERS = {"User-Agent": "InventoryLab/1.0 (student project)"}


def get_product_by_barcode(barcode):
    # Returns a product dictionary, or None if not found or if the API fails
    url = BASE_URL + "/api/v0/product/" + barcode + ".json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        data = response.json()
    except Exception as error:
        print("Could not reach OpenFoodFacts:", error)
        return None

    # status 1 means the product was found, status 0 means not found
    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    # Only keep the information we need
    return {
        "barcode": barcode,
        "product_name": product.get("product_name", ""),
        "brands": product.get("brands", ""),
        "ingredients_text": product.get("ingredients_text", "")
    }


def search_products_by_name(name):
    # Returns a list of products (the list is empty if nothing was found)
    url = BASE_URL + "/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "json": 1,
        "page_size": 5
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = response.json()
    except Exception as error:
        print("Could not reach OpenFoodFacts:", error)
        return []

    results = []
    for product in data.get("products", []):
        results.append({
            "barcode": product.get("code", ""),
            "product_name": product.get("product_name", ""),
            "brands": product.get("brands", "")
        })
    return results
