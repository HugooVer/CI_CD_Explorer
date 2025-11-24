from fastapi.testclient import TestClient
from app.main import (
    app,
    to_fahrenheit,
    to_celsius,
    cups_to_ml,
    ml_to_cups,
    CUP_ML,
)

client = TestClient(app)


# --- Convert test ---


def test_to_fahrenheit_function():
    assert to_fahrenheit(0) == 32
    assert to_fahrenheit(100) == 212


def test_to_celsius_function():
    assert to_celsius(32) == 0
    assert to_celsius(212) == 100


def test_cups_to_ml_function():
    assert cups_to_ml(1) == CUP_ML
    assert cups_to_ml(2) == 2 * CUP_ML


def test_ml_to_cups_function():
    assert ml_to_cups(CUP_ML) == 1
    assert ml_to_cups(2 * CUP_ML) == 2


# --- Test API conversion ---


def test_convert_celsius_to_fahrenheit():
    resp = client.get("/convert?celsius=0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "temperature"
    assert data["input_unit"] == "celsius"
    assert data["output_unit"] == "fahrenheit"
    assert data["input_value"] == 0
    assert data["output_value"] == 32


def test_convert_fahrenheit_to_celsius():
    resp = client.get("/convert?fahrenheit=32")
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "temperature"
    assert data["input_unit"] == "fahrenheit"
    assert data["output_unit"] == "celsius"
    assert data["input_value"] == 32
    assert data["output_value"] == 0


def test_convert_cup_to_ml():
    resp = client.get("/convert?cup=2")
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "volume"
    assert data["input_unit"] == "cup"
    assert data["output_unit"] == "ml"
    assert data["input_value"] == 2
    assert data["output_value"] == 2 * CUP_ML


def test_convert_ml_to_cup():
    resp = client.get(f"/convert?ml={2 * CUP_ML}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "volume"
    assert data["input_unit"] == "ml"
    assert data["output_unit"] == "cup"
    assert data["input_value"] == 2 * CUP_ML
    assert data["output_value"] == 2


def test_convert_no_parameter():
    resp = client.get("/convert")
    assert resp.status_code == 400
    data = resp.json()
    assert "Provide exactly one" in data["detail"]


def test_convert_multiple_parameters():
    resp = client.get("/convert?celsius=0&ml=100")
    assert resp.status_code == 400
    data = resp.json()
    assert "Provide only one" in data["detail"]
