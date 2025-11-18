import pytest
from app import exchange


class Response:
    def __init__(self, status_code=200, data=None, text=""):
        self.status_code = status_code
        self._data = data or {}
        self.text = text

    def json(self):
        return self._data


def test_get_exchange_data_success(monkeypatch):
    dummy_data = {
        "success": True,
        "source": "USD",
        "timestamp": 1700000000,
        "quotes": {
            "USDEGP": 47.123456,
            "USDEUR": 0.912345,
        },
    }

    def fake_get(url, params=None, timeout=None):
        return Response(200, dummy_data)

    monkeypatch.setattr(exchange, "EXCHANGE_API_KEY", "test-key")
    monkeypatch.setattr(exchange.requests, "get", fake_get)

    records = exchange.get_exchange_data(base="USD")
    assert isinstance(records, list)
    assert {r["code"] for r in records} == {"EGP", "EUR"}


def test_get_exchange_data_api_error(monkeypatch):
    dummy_data = {"success": False, "error": {"info": "Invalid key"}}

    def fake_get(url, params=None, timeout=None):
        return Response(200, dummy_data)

    monkeypatch.setattr(exchange, "EXCHANGE_API_KEY", "bad-key")
    monkeypatch.setattr(exchange.requests, "get", fake_get)

    result = exchange.get_exchange_data()
    assert isinstance(result, dict)
    assert "error" in result


def test_plot_exchange_bar(tmp_path):
    records = [
        {"timestamp": 1, "base": "USD", "code": "EGP", "pair": "USD:EGP", "rate": 47.12},
        {"timestamp": 1, "base": "USD", "code": "EUR", "pair": "USD:EUR", "rate": 0.91},
    ]
    img_b64 = exchange.plot_exchange_bar(records)
    assert isinstance(img_b64, str)
    assert img_b64 != ""


def test_save_exchange_csv(tmp_path):
    records = [
        {"timestamp": 1, "base": "USD", "code": "EGP", "pair": "USD:EGP", "rate": 47.12}
    ]
    csv_path = tmp_path / "exchange.csv"
    result = exchange.save_exchange_csv(records, str(csv_path))
    assert result == {"ok": True}
    assert csv_path.exists()
