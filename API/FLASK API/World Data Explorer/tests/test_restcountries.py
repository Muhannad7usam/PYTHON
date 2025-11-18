import pytest

from app import restcountries


class DummyResponse:
    def __init__(self, status_code=200, data=None, text=""):
        self.status_code = status_code
        self._data = data or {}
        self.text = text

    def json(self):
        return self._data


def test_get_country_data_success(monkeypatch):
    dummy_country = [
        {
            "name": {"common": "Egypt"},
            "capital": ["Cairo"],
            "region": "Africa",
            "subregion": "Northern Africa",
            "population": 100000000,
            "area": 1000000.0,
            "languages": {"ara": "Arabic"},
            "currencies": {"EGP": {"name": "Egyptian pound"}},
            "flags": {"png": "http://flag.png"},
        }
    ]

    def fake_get(url, timeout=None):
        return DummyResponse(200, dummy_country)

    monkeypatch.setattr(restcountries.requests, "get", fake_get)

    result = restcountries.get_country_data("Egypt")
    assert result["name"] == "Egypt"
    assert result["capital"] == "Cairo"
    assert result["population_raw"] == 100000000
    assert "km²" in result["area_formatted"]
    assert "Arabic" in result["languages"]
    assert "Egyptian pound" in result["currencies"]
    assert result["flag"] == "http://flag.png"


def test_get_country_data_http_error(monkeypatch):
    def fake_get(url, timeout=None):
        return DummyResponse(404, {}, "Not found")

    monkeypatch.setattr(restcountries.requests, "get", fake_get)

    result = restcountries.get_country_data("Nowhere")
    assert "error" in result


def test_plot_population_pie_returns_image_for_multiple():
    countries = [
        {"name": "A", "population_raw": 10},
        {"name": "B", "population_raw": 20},
    ]
    img_b64 = restcountries.plot_population_pie(countries)
    assert isinstance(img_b64, str)
    assert len(img_b64) > 0


def test_plot_population_pie_returns_none_for_zero_pop():
    countries = [
        {"name": "A", "population_raw": 0},
        {"name": "B", "population_raw": 0},
    ]
    assert restcountries.plot_population_pie(countries) is None


def test_plot_area_bar_returns_image():
    countries = [
        {"name": "A", "area_raw": 100.0},
        {"name": "B", "area_raw": 200.0},
    ]
    img_b64 = restcountries.plot_area_bar(countries)
    assert isinstance(img_b64, str)
    assert len(img_b64) > 0


def test_plot_area_bar_returns_none_for_zero_area():
    countries = [{"name": "A", "area_raw": 0}]
    assert restcountries.plot_area_bar(countries) is None


def test_save_countries_csv_excel_writes_csv(tmp_path):
    records = [
        {
            "name": "Egypt",
            "capital": "Cairo",
            "region": "Africa",
            "subregion": "Northern Africa",
            "population_raw": 100000000,
            "area_raw": 1000000.0,
            "languages": "Arabic",
            "currencies": "Egyptian pound (EGP)",
            "flag": "http://flag.png",
        }
    ]
    csv_path = tmp_path / "countries.csv"
    xlsx_path = tmp_path / "countries.xlsx"
    res = restcountries.save_countries_csv_excel(records, str(csv_path), str(xlsx_path))
    assert res == {"ok": True}
    assert csv_path.exists()
