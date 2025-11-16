import requests
import base64
import os
import io
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OWM_API_KEY = os.getenv("OPENWEATHER_API_KEY")

WEATHER_STORE = []


def get_weather_data(lat, lon, units="metric", lang=None, display_name=None, timeout=20):
    if not OWM_API_KEY:
        return {"error": "OPENWEATHER_API_KEY is not set."}

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OWM_API_KEY,
        "units": units,
    }
    if lang:
        params["lang"] = lang

    url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        resp = requests.get(url, params=params, timeout=timeout)
    except Exception as e:
        return {"error": f"Error connecting to OpenWeather API: {str(e)}."}

    if resp.status_code != 200:
        return {
            "error": f"Failed to fetch weather data: HTTP {resp.status_code}.",
            "message": resp.text[:500],
        }

    data = resp.json() or {}
    main = data.get("main") or {}
    weather_list = data.get("weather") or []
    desc = weather_list[0].get("description") if weather_list else ""

    result = {
        "display_name": display_name or f"{lat},{lon}",
        "lat": lat,
        "lon": lon,
        "temperature_celsius_raw": main.get("temp"),
        "humidity": main.get("humidity"),
        "weather_description": desc,
    }

    WEATHER_STORE.append(result)

    return result


def get_cached_weather():
    return list(WEATHER_STORE)


def plot_clustered_comparison(weather_data):
    if not weather_data:
        return None

    cities = [w.get("display_name", "") for w in weather_data]
    temps = [w.get("temperature_celsius_raw", 0) for w in weather_data]
    hums = [w.get("humidity", 0) for w in weather_data]

    x = range(len(cities))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar([i - width / 2 for i in x], temps, width, label="Temp (°C)")
    ax.bar([i + width / 2 for i in x], hums, width, label="Humidity (%)")

    ax.set_xticks(list(x))
    ax.set_xticklabels(cities)
    ax.set_ylabel("Value")
    ax.set_title("Weather Comparison")
    ax.legend()
    ax.tick_params(axis="x", labelrotation=45)

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode("utf-8")


def save_weather_csv(weather_data, csv_path):
    if not weather_data:
        return {"error": "No data to save."}

    try:
        fieldnames = [
            "display_name",
            "lat",
            "lon",
            "temperature_celsius_raw",
            "humidity",
            "weather_description",
        ]
        with open(csv_path, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for w in weather_data:
                writer.writerow(
                    {
                        "display_name": w.get("display_name", ""),
                        "lat": w.get("lat", ""),
                        "lon": w.get("lon", ""),
                        "temperature_celsius_raw": w.get(
                            "temperature_celsius_raw", ""
                        ),
                        "humidity": w.get("humidity", ""),
                        "weather_description": w.get("weather_description", ""),
                    }
                )
        return {"ok": True}
    except Exception as e:
        return {"error": str(e)}
