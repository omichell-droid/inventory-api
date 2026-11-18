# app.py
# The Flask REST API for the inventory system.
# Start it with:  python app.py

from flask import Flask, jsonify, request

from data import inventory, get_next_id, find_item
from external_api import get_product_by_barcode, search_products_by_name

app = Flask(__name__)


# ---------- READ: get all items ----------
@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200


# ---------- READ: get one item ----------
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_one_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


# ---------- CREATE: add a new item ----------
@app.route("/inventory", methods=["POST"])
def add_item():
    new_data = request.get_json(silent=True)

    # Check that we got data and a product name
    if new_data is None or "product_name" not in new_data:
        return jsonify({"error": "product_name is required"}), 400

    new_item = {
        "id": get_next_id(),
        "barcode": new_data.get("barcode", ""),
        "product_name": new_data["product_name"],
        "brands": new_data.get("brands", ""),
        "ingredients_text": new_data.get("ingredients_text", ""),
        "price": new_data.get("price", 0),
        "stock": new_data.get("stock", 0)
    }

    inventory.append(new_item)
    return jsonify(new_item), 201


# ---------- UPDATE: change an item ----------
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    new_data = request.get_json(silent=True)
    if new_data is None:
        return jsonify({"error": "No data sent"}), 400

    # Only update the fields that were sent (the id can never change)
    if "product_name" in new_data:
        item["product_name"] = new_data["product_name"]
    if "brands" in new_data:
        item["brands"] = new_data["brands"]
    if "price" in new_data:
        item["price"] = new_data["price"]
    if "stock" in new_data:
        item["stock"] = new_data["stock"]

    return jsonify(item), 200


# ---------- DELETE: remove an item ----------
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": "Item deleted"}), 200


# ---------- HELPER: search OpenFoodFacts ----------
# Examples:  /external/search?barcode=3017620422003
#            /external/search?name=almond milk
@app.route("/external/search", methods=["GET"])
def search_external():
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if barcode:
        product = get_product_by_barcode(barcode)
        if product is None:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product), 200

    if name:
        products = search_products_by_name(name)
        return jsonify(products), 200

    return jsonify({"error": "Please give a barcode or a name"}), 400


# ---------- HELPER: import a product from OpenFoodFacts ----------
# Gets the product by barcode and adds it to our inventory list
@app.route("/inventory/import", methods=["POST"])
def import_item():
    new_data = request.get_json(silent=True)
    if new_data is None or "barcode" not in new_data:
        return jsonify({"error": "barcode is required"}), 400

    product = get_product_by_barcode(new_data["barcode"])
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    new_item = {
        "id": get_next_id(),
        "barcode": product["barcode"],
        "product_name": product["product_name"],
        "brands": product["brands"],
        "ingredients_text": product["ingredients_text"],
        "price": new_data.get("price", 0),
        "stock": new_data.get("stock", 0)
    }

    inventory.append(new_item)
    return jsonify(new_item), 201


if __name__ == "__main__":
    # debug=True restarts the server when you save and shows helpful errors
    app.run(debug=True, port=5000)
