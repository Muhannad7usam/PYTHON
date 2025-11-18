import pytest

from app import weather


class Response:
    def __init__(self, status_code=200, data=None, text=""):
        self.status_code = status_code
        self._data = data or {}
        self.text = text

    def json(self):
        return self._data


def test_get_weather_data_missing_api_key(monkeypatch):
    monkeypatch.setattr(weather, "OWM_API_KEY", None)
    result = weather.get_weather_data(30.0, 31.0)
    assert "error" in result
    assert "OPENWEATHER_API_KEY" in result["error"]


def test_get_weather_data_success(monkeypatch):
    data = {
        "main": {"temp": 25.5, "humidity": 60},
        "weather": [{"description": "clear sky"}],
    }

    def fake_get(url, params=None, timeout=None):
        return Response(200, data)

    monkeypatch.setattr(weather, "OWM_API_KEY", "dummy-key")
    monkeypatch.setattr(weather.requests, "get", fake_get)

    result = weather.get_weather_data(30.0, 31.0, display_name="Cairo")
    assert result["display_name"] == "Cairo"
    assert result["temperature_celsius_raw"] == pytest.approx(25.5)
    assert result["humidity"] == 60
    assert result["weather_description"] == "clear sky"


def test_get_weather_data_http_error(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        return Response(404, {}, "error")

    monkeypatch.setattr(weather, "OWM_API_KEY", "dummy-key")
    monkeypatch.setattr(weather.requests, "get", fake_get)

    result = weather.get_weather_data(0, 0)
    assert "error" in result
    assert result["error"].startswith("Failed to fetch weather data")


def test_plot_clustered_comparison_returns_image():
    data = [
        {
            "display_name": "City A",
            "lat": 1.0,
            "lon": 2.0,
            "temperature_celsius_raw": 20.0,
            "humidity": 50,
            "weather_description": "sunny",
        },
        {
            "display_name": "City B",
            "lat": 3.0,
            "lon": 4.0,
            "temperature_celsius_raw": 25.0,
            "humidity": 70,
            "weather_description": "cloudy",
        },
    ]
    img_b64 = weather.plot_clustered_comparison(data)
    assert isinstance(img_b64, str)
    assert len(img_b64) > 0


def test_plot_clustered_comparison_none_for_empty():
    assert weather.plot_clustered_comparison([]) is None


def test_save_weather_csv_success(tmp_path):
    data = [
        {
            "display_name": "City A",
            "lat": 1.0,
            "lon": 2.0,
            "temperature_celsius_raw": 20.0,
            "humidity": 50,
            "weather_description": "sunny",
        }
    ]
    csv_path = tmp_path / "weather.csv"
    res = weather.save_weather_csv(data, str(csv_path))
    assert res == {"ok": True}
    assert csv_path.exists()
