import pytest
from app import covid


class Response:
    def __init__(self, status_code=200, data=None, text=""):
        self.status_code = status_code
        self._data = data or {}
        self.text = text

    def json(self):
        return self._data


def test_get_covid_data_success(monkeypatch):
    dummy_data = {
        "timeline": {
            "cases": {"1/1/20": 10, "1/2/20": 15},
            "deaths": {"1/1/20": 1, "1/2/20": 2},
            "recovered": {"1/1/20": 0, "1/2/20": 5},
        }
    }

    def fake_get(url, params=None, timeout=None):
        return Response(200, dummy_data)

    monkeypatch.setattr(covid.requests, "get", fake_get)

    records = covid.get_covid_data()
    assert isinstance(records, list)
    assert len(records) == 2
    assert records[0]["cases_total"] == 10
    assert records[1]["cases_total"] == 15


def test_get_covid_data_http_error(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        return Response(500, {}, "server error")

    monkeypatch.setattr(covid.requests, "get", fake_get)

    result = covid.get_covid_data()
    assert isinstance(result, dict)
    assert "error" in result


def test_plot_covid_graph(monkeypatch):
    records = [
        {
            "date": "1/1/20",
            "cases_total": 10,
            "deaths_total": 1,
            "recovered_total": 0,
            "cases_new": 0,
            "deaths_new": 0,
            "recovered_new": 0,
        },
        {
            "date": "1/2/20",
            "cases_total": 20,
            "deaths_total": 2,
            "recovered_total": 5,
            "cases_new": 10,
            "deaths_new": 1,
            "recovered_new": 5,
        },
    ]

    img_b64 = covid.plot_covid_graph(records)
    assert isinstance(img_b64, str)
    assert img_b64 != ""


def test_save_covid_csv(tmp_path):
    records = [
        {
            "date": "1/1/20",
            "cases_total": 10,
            "deaths_total": 1,
            "recovered_total": 0,
            "cases_new": 0,
            "deaths_new": 0,
            "recovered_new": 0,
        }
    ]
    csv_path = tmp_path / "covid.csv"
    result = covid.save_covid_csv(records, str(csv_path))
    assert result == {"ok": True}
    assert csv_path.exists()
