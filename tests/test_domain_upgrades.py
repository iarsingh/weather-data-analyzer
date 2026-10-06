import pytest
from fastapi.testclient import TestClient
from weather.main import app

client = TestClient(app)


def test_non_finite_and_boolean_temperatures_are_skipped():
    r = client.post("/analyze", json={"rows": [{"temp_c": "NaN"}, {"temp_c": "Infinity"}, {"temp_c": True}, {"city": " Delhi ", "temp_c": 20}]}).json()
    assert r["valid_rows"] == 1 and r["skipped"] == 3
    assert r["by_city"] == {"Delhi": 20.0}
    assert r["city_counts"] == {"Delhi": 1}


def test_statistics_are_reconciled():
    r = client.post("/analyze", json={"rows": [{"city": None, "temp_c": 10}, {"city": "", "temp_c": 30}]}).json()
    assert r["median"] == 20 and r["stddev"] == 10
    assert r["rows"] == r["valid_rows"] + r["skipped"]
    assert r["city_counts"] == {"unknown": 2}


def test_out_of_range_and_large_requests_are_rejected():
    assert client.post("/analyze", json={"rows": [{"temp_c": 200}]}).status_code == 422
    assert client.post("/analyze", json={"rows": [{"temp_c": 20}] * 10001}).status_code == 422
