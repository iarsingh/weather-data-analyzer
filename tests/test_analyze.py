from fastapi.testclient import TestClient
from weather.main import app

client = TestClient(app)


def test_summary():
    payload = client.post("/analyze", json={"rows": [{'city': 'delhi', 'temp_c': 32}, {'city': 'delhi', 'temp_c': 28}, {'city': 'pune', 'temp_c': 30}]}).json()
    assert payload["mean"] == 30.0
    assert payload["by_city"]["delhi"]


def test_empty_is_refused():
    assert client.post("/analyze", json={"rows": []}).status_code == 422
