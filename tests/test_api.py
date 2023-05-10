import logging
from typing import List

from demo_db_api.api import app
from demo_db_api.routers import get_db
from demo_db_api.schemas import response


def test_get_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"msg": "Hello, data science."}


def test_get_available_dbs(caplog, client):
    caplog.set_level(logging.DEBUG)
    resp = client.get("/v1/availability")
    assert resp.status_code == 200

    message = resp.json()
    assert "meta" in message.keys()
    
    # Make sure a data message is returned
    assert "data" in message.keys()
    assert "dataSets" in message.get("data").keys()
    assert isinstance(message.get("data").get("dataSets"), List)

    # Expecting only a single dataset to be present
    assert len(message.get("data").get("dataSets")) == 1