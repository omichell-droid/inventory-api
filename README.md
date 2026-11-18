# Inventory Management System (Flask REST API)

A simple inventory system for a small shop. Staff can add, view, update and delete products using a command-line menu. The menu talks to a Flask API. Product details can also be looked up from the [OpenFoodFacts API](https://world.openfoodfacts.org) and added to the inventory.

## Files

| File | What it does |
|---|---|
| `app.py` | The Flask API (all the routes) |
| `data.py` | The inventory list (our pretend database) |
| `external_api.py` | Gets product data from OpenFoodFacts |
| `cli.py` | The menu you use in the terminal |
| `tests/` | The tests (run with pytest) |

## Setup (Mac)

```bash
git clone https://github.com/YOUR-USERNAME/inventory-api.git
cd inventory-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to run

1. Start the server:
   ```bash
   python app.py
   ```
2. Open a new terminal tab, then start the menu:
   ```bash
   source venv/bin/activate
   python cli.py
   ```

To run the tests:
```bash
pytest -v
```

## API Routes

| Method | Route | What it does |
|---|---|---|
| GET | `/inventory` | Get all items |
| GET | `/inventory/<id>` | Get one item |
| POST | `/inventory` | Add a new item |
| PATCH | `/inventory/<id>` | Update an item |
| DELETE | `/inventory/<id>` | Delete an item |
| GET | `/external/search?barcode=<barcode>` | Look up a product on OpenFoodFacts by barcode |
| GET | `/external/search?name=<name>` | Search OpenFoodFacts by name |
| POST | `/inventory/import` | Get a product from OpenFoodFacts and add it to the inventory |

### Example: add an item (POST /inventory)
```json
{"product_name": "Bread", "brands": "Bakery", "price": 2.5, "stock": 10}
```

### Example: update stock (PATCH /inventory/1)
```json
{"stock": 45}
```

### Example: import from OpenFoodFacts (POST /inventory/import)
```json
{"barcode": "3017620422003", "price": 6.49, "stock": 20}
```

### Example item in the inventory
```json
{
  "id": 1,
  "barcode": "0025293001404",
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
  "price": 4.99,
  "stock": 50
}
```

## Using the CLI

```
===== Inventory Admin =====
1. View all items
2. View one item
3. Add an item
4. Update price or stock
5. Delete an item
6. Search OpenFoodFacts
7. Import an item from OpenFoodFacts
0. Exit
```

Example:
```
Choose an option: 7
Enter barcode: 3017620422003
Price: 6.49
Stock: 20
Imported and added to inventory:
[4] Nutella - Ferrero | Price: 6.49 | Stock: 20
```

- If you type something that isn't a number for price or stock, the menu asks again.
- If the server isn't running, you'll see: "Cannot connect. Is the Flask server running?"

## Notes
- The data is stored in a Python list, so it resets when the server restarts.
- On a Mac, if port 5000 is busy, turn off AirPlay Receiver in System Settings → General → AirDrop & Handoff.
