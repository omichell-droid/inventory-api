# conftest.py
# pytest runs this file automatically. It gives every test a fresh
# copy of the starting data, so one test can't break another.

import copy

import pytest

import data
from app import app

STARTING_DATA = copy.deepcopy(data.inventory)


@pytest.fixture
def client():
    # Put the list back to how it started
    data.inventory.clear()
    data.inventory.extend(copy.deepcopy(STARTING_DATA))

    # A fake browser we can send requests with
    app.config["TESTING"] = True
    return app.test_client()
