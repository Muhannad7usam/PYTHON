import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
import csv

FIELDS = "name,capital,region,subregion,population,area,languages,currencies,flags"

COUNTRY_STORE = []


def get_country_data(country_name):
    try:
        url = f"https://restcountries.com/v3.1/name/{country_name}?fields={FIELDS}"
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return {
                "error": f"Couldn’t fetch data. Server responded with {response.status_code}.",
                "message": response.text,
            }

        data = response.json()
        if not data:
            return {"error": "No data returned."}

        country = data[0]

        name = country.get("name", {}).get("common", "Unknown Country")
        capital_list = country.get("capital") or []
        capital = capital_list[0] if capital_list else "N/A"
        region = country.get("region", "")
        subregion = country.get("subregion", "")
        population = int(country.get("population", 0))
        area = float(country.get("area", 0.0))

        langs = country.get("languages") or {}
        languages = ", ".join(langs.values()) if langs else ""

        curr = country.get("currencies") or {}
        currency_parts = []
        for code, info in curr.items():
            nm = info.get("name", code)
            currency_parts.append(f"{nm} ({code})")
        currencies = ", ".join(currency_parts) if currency_parts else ""

        flag = (country.get("flags") or {}).get("png", "")

        record = {
            "name": name,
            "capital": capital,
            "region": region,
            "subregion": subregion,
            "population_raw": population,
            "area_raw": area,
            "area_formatted": f"{area:,.0f} km²" if area else "0 km²",
            "languages": languages,
            "currencies": currencies,
            "flag": flag,
        }

        COUNTRY_STORE.clear()
        COUNTRY_STORE.append(record)

        return record

    except Exception as e:
        return {"error": f"Error fetching country data: {str(e)}"}


def get_cached_country():
    return COUNTRY_STORE[0] if COUNTRY_STORE else None


def plot_population_pie(countries):
    if not countries:
        return None

    labels = []
    values = []
    for c in countries:
        pop = int(c.get("population_raw", 0) or 0)
        if pop > 0:
            labels.append(c.get("name", ""))
            values.append(pop)

    if not values:
        return None

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(values, labels=labels, autopct="%1.1f%%")
    ax.set_title("Population Comparison")

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode("utf-8")


def plot_area_bar(countries):
    if not countries:
        return None

    labels = []
    values = []
    for c in countries:
        area = float(c.get("area_raw", 0.0) or 0.0)
        if area > 0:
            labels.append(c.get("name", ""))
            values.append(area)

    if not values:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values)
    ax.set_xlabel("Country")
    ax.set_ylabel("Area (km²)")
    ax.set_title("Country Areas")
    ax.tick_params(axis="x", labelrotation=45)

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode("utf-8")


def save_countries_csv_excel(records, csv_path, xlsx_path):
    if not records:
        return {"error": "No records to save."}

    try:
        cols = [
            "name",
            "capital",
            "region",
            "subregion",
            "population_raw",
            "area_raw",
            "languages",
            "currencies",
            "flag",
        ]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cols)
            writer.writeheader()
            for r in records:
                row = {c: r.get(c, "") for c in cols}
                writer.writerow(row)

        return {"ok": True}
    except Exception as e:
        return {"error": f"Error saving CSV: {str(e)}."}
