import logging
from typing import List

from demo_db_api.api import app
from demo_db_api.routers import get_db


def test_get_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello, data science."}


def test_get_available_dbs(caplog, client):
    caplog.set_level(logging.DEBUG)
    response = client.get("/v1/availability")
    assert response.status_code == 200

    dbs = response.json()
    assert isinstance(dbs, List)
    
    # There should only be a single table in the test database
    assert dbs[0].get("db") == "wes"
    assert dbs[0].get("freq") == "monthly"