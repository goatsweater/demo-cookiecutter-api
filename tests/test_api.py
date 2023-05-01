from fastapi.testclient import TestClient

from demo_cookiecutter_api.api import app

client = TestClient(app)


def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello, data science."}
