# data.py
# This list is our "database". It only lives in memory,
# so it resets every time the server restarts.
# Each item looks like a product from OpenFoodFacts, plus an id, price and stock.

inventory = [
    {
        "id": 1,
        "barcode": "0025293001404",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
        "price": 4.99,
        "stock": 50
    },
    {
        "id": 2,
        "barcode": "3017620422003",
        "product_name": "Nutella",
        "brands": "Ferrero",
        "ingredients_text": "Sugar, palm oil, hazelnuts, skimmed milk powder, cocoa",
        "price": 6.49,
        "stock": 30
    },
    {
        "id": 3,
        "barcode": "5449000000996",
        "product_name": "Coca-Cola Original",
        "brands": "Coca-Cola",
        "ingredients_text": "Carbonated water, sugar, caramel colour, phosphoric acid",
        "price": 1.25,
        "stock": 120
    }
]


def get_next_id():
    # Find the biggest id in the list and add 1
    biggest_id = 0
    for item in inventory:
        if item["id"] > biggest_id:
            biggest_id = item["id"]
    return biggest_id + 1


def find_item(item_id):
    # Look through the list for an item with this id
    for item in inventory:
        if item["id"] == item_id:
            return item
    # If we get here, the item was not found
    return None
