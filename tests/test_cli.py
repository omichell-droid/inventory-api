# test_cli.py
# Tests for cli.py. We fake the user's typing (input) and the
# server's answers (requests), then check what gets printed.

from unittest.mock import Mock, patch

import requests

import cli

ONE_ITEM = {"id": 1, "product_name": "Milk", "brands": "Silk",
            "price": 4.99, "stock": 50, "ingredients_text": "water"}


def make_fake_response(status_code, json_data):
    fake_response = Mock()
    fake_response.status_code = status_code
    fake_response.json.return_value = json_data
    return fake_response


@patch("cli.requests.get")
def test_view_all_items(fake_get, capsys):
    fake_get.return_value = make_fake_response(200, [ONE_ITEM])
    cli.view_all_items()
    output = capsys.readouterr().out
    assert "Milk" in output


@patch("cli.requests.get")
def test_server_not_running(fake_get, capsys):
    fake_get.side_effect = requests.exceptions.ConnectionError()
    cli.view_all_items()
    output = capsys.readouterr().out
    assert "Is the Flask server running?" in output


@patch("cli.requests.post")
@patch("builtins.input")
def test_add_item(fake_input, fake_post, capsys):
    # The user types: name, brand, price, stock
    fake_input.side_effect = ["Bread", "Bakery", "2.50", "10"]
    fake_post.return_value = make_fake_response(201, ONE_ITEM)

    cli.add_item()

    assert "Item added" in capsys.readouterr().out
    sent_data = fake_post.call_args.kwargs["json"]
    assert sent_data["product_name"] == "Bread"
    assert sent_data["stock"] == 10


@patch("cli.requests.patch")
@patch("builtins.input")
def test_update_stock(fake_input, fake_patch, capsys):
    # The user types: id 1, no to price, yes to stock, new stock 20
    fake_input.side_effect = ["1", "n", "y", "20"]
    fake_patch.return_value = make_fake_response(200, ONE_ITEM)

    cli.update_item()

    assert fake_patch.call_args.kwargs["json"] == {"stock": 20}


@patch("cli.requests.delete")
@patch("builtins.input")
def test_delete_item(fake_input, fake_delete, capsys):
    fake_input.side_effect = ["2", "y"]
    fake_delete.return_value = make_fake_response(200, {"message": "Item deleted"})

    cli.delete_item()

    assert "Item deleted" in capsys.readouterr().out


@patch("cli.requests.get")
@patch("builtins.input")
def test_search_by_barcode(fake_input, fake_get, capsys):
    fake_input.side_effect = ["3017620422003"]
    fake_get.return_value = make_fake_response(
        200, {"product_name": "Nutella", "brands": "Ferrero", "ingredients_text": "sugar"})

    cli.search_openfoodfacts()

    assert "Nutella" in capsys.readouterr().out


@patch("cli.requests.post")
@patch("builtins.input")
def test_import_item(fake_input, fake_post, capsys):
    fake_input.side_effect = ["3017620422003", "6.49", "20"]
    fake_post.return_value = make_fake_response(201, ONE_ITEM)

    cli.import_from_openfoodfacts()

    assert "Imported" in capsys.readouterr().out


@patch("builtins.input")
def test_number_input_asks_again_if_wrong(fake_input):
    # First two answers are wrong, the third is right
    fake_input.side_effect = ["abc", "-5", "3.5"]
    assert cli.ask_for_number("Price: ") == 3.5


@patch("builtins.input")
def test_menu_invalid_option_then_exit(fake_input, capsys):
    fake_input.side_effect = ["9", "0"]
    cli.main()
    output = capsys.readouterr().out
    assert "Invalid option" in output
    assert "Goodbye!" in output
