# cli.py
# A simple menu in the terminal that talks to our Flask API.
# 1. Start the server first:  python app.py
# 2. Then in a new terminal:  python cli.py

import requests

API_URL = "http://127.0.0.1:5000"


def print_item(item):
    print(f"[{item['id']}] {item['product_name']} - {item['brands']} | "
          f"Price: {item['price']} | Stock: {item['stock']}")


def ask_for_number(message):
    # Keep asking until the user types a valid number
    while True:
        answer = input(message)
        try:
            number = float(answer)
            if number >= 0:
                return number
            print("Please enter a number that is 0 or more.")
        except ValueError:
            print("That is not a number. Try again.")


def ask_for_whole_number(message):
    # Keep asking until the user types a whole number like 5
    while True:
        answer = input(message)
        if answer.isdigit():
            return int(answer)
        print("Please enter a whole number like 5.")


def view_all_items():
    try:
        response = requests.get(API_URL + "/inventory")
    except requests.exceptions.ConnectionError:
        print("Cannot connect. Is the Flask server running?")
        return

    items = response.json()
    if len(items) == 0:
        print("The inventory is empty.")
    for item in items:
        print_item(item)


def view_one_item():
    item_id = ask_for_whole_number("Enter item ID: ")
    try:
        response = requests.get(API_URL + "/inventory/" + str(item_id))
    except requests.exceptions.ConnectionError:
        print("Cannot connect. Is the Flask server running?")
        return

    if response.status_code == 404:
        print("Item not found.")
    else:
        item = response.json()
        print_item(item)
        print("Ingredients:", item["ingredients_text"])


def add_item():
    name = input("Product name: ")
    if name == "":
        print("Product name cannot be empty.")
        return

    new_item = {
        "product_name": name,
        "brands": input("Brand: "),
        "price": ask_for_number("Price: "),
        "stock": ask_for_whole_number("Stock: ")
    }

    try:
        response = requests.post(API_URL + "/inventory", json=new_item)
    except requests.exceptions.ConnectionError:
        print("Cannot connect. Is the Flask server running?")
        return

    if response.status_code == 201:
        print("Item added:")
        print_item(response.json())
    else:
        print("Error:", response.json()["error"])


def update_item():
    item_id = ask_for_whole_number("Enter item ID to update: ")
    changes = {}

    if input("Change the price? (y/n): ") == "y":
        changes["price"] = ask_for_number("New price: ")
    if input("Change the stock? (y/n): ") == "y":
        changes["stock"] = ask_for_whole_number("New stock: ")

    if len(changes) == 0:
        print("Nothing to update.")
        return

    try:
        response = requests.patch(API_URL + "/inventory/" + str(item_id), json=changes)
    except requests.exceptions.ConnectionError:
        print("Cannot connect. Is the Flask server running?")
        return

    if response.status_code == 404:
        print("Item not found.")
    else:
        print("Item updated:")
        print_item(response.json())


def delete_item():
    item_id = ask_for_whole_number("Enter item ID to delete: ")
    sure = input("Are you sure? (y/n): ")
    if sure != "y":
        print("Delete cancelled.")
        return

    try:
        response = requests.delete(API_URL + "/inventory/" + str(item_id))
    except requests.exceptions.ConnectionError:
        print("Cannot connect. Is the Flask server running?")
        return

    if response.status_code == 404:
        print("Item not found.")
    else:
        print("Item deleted.")


def search_openfoodfacts():
    search = input("Enter a barcode or product name: ")
    if search == "":
        print("Please type something to search for.")
        return

    # If it's all digits, treat it as a barcode, otherwise as a name
    if search.isdigit():
        params = {"barcode": search}
    else:
        params = {"name": search}

    try:
        response = requests.get(API_URL + "/external/search", params=params)
    except requests.exceptions.ConnectionError:
        print("Cannot connect. Is the Flask server running?")
        return

    if response.status_code != 200:
        print("Product not found.")
        return

    result = response.json()
    if search.isdigit():
        print(f"{result['product_name']} - {result['brands']}")
        print("Ingredients:", result["ingredients_text"])
    else:
        if len(result) == 0:
            print("No products found.")
        for product in result:
            print(f"{product['product_name']} - {product['brands']} (barcode {product['barcode']})")


def import_from_openfoodfacts():
    barcode = input("Enter barcode: ")
    if not barcode.isdigit():
        print("A barcode should only contain numbers.")
        return

    new_item = {
        "barcode": barcode,
        "price": ask_for_number("Price: "),
        "stock": ask_for_whole_number("Stock: ")
    }

    try:
        response = requests.post(API_URL + "/inventory/import", json=new_item)
    except requests.exceptions.ConnectionError:
        print("Cannot connect. Is the Flask server running?")
        return

    if response.status_code == 201:
        print("Imported and added to inventory:")
        print_item(response.json())
    else:
        print("Product not found on OpenFoodFacts.")


def main():
    while True:
        print("")
        print("===== Inventory Admin =====")
        print("1. View all items")
        print("2. View one item")
        print("3. Add an item")
        print("4. Update price or stock")
        print("5. Delete an item")
        print("6. Search OpenFoodFacts")
        print("7. Import an item from OpenFoodFacts")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            view_all_items()
        elif choice == "2":
            view_one_item()
        elif choice == "3":
            add_item()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            search_openfoodfacts()
        elif choice == "7":
            import_from_openfoodfacts()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
