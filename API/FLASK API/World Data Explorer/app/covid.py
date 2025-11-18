import io
import csv
import base64
import requests

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
from datetime import datetime

COVID_BASE_URL = "https://disease.sh/v3/covid-19/historical"

COVID_STORE = []    
def get_covid_data(country=None, timeout=20):
    if country:
        url = f"{COVID_BASE_URL}/{country}"
    else:
        url = f"{COVID_BASE_URL}/all"

    params = {"lastdays": "all"}

    try:
        r = requests.get(url, params=params, timeout=timeout)
    except Exception as e:
        return {"error": f"Error connecting to COVID API: {str(e)}."}

    if r.status_code != 200:
        return {
            "error": f"COVID API returned HTTP {r.status_code}.",
            "message": r.text[:500],
        }

    data = r.json() or {}

    cases_raw = data.get("cases") or {}
    deaths_raw = data.get("deaths") or {}
    recovered_raw = data.get("recovered") or {}

    dates = list(cases_raw.keys())

    def _sort_key(d):
        p = str(d).split("/")
        if len(p) != 3:
            return (0, 0, 0)
        m = int(p[0])
        day = int(p[1])
        y = int(p[2])
        year = y + (2000 if y < 100 else 0)
        return (year, m, day)

    dates.sort(key=_sort_key)

    records = []
    prev_cases = None
    prev_deaths = None
    prev_recovered = None

    for d in dates:
        c = int(cases_raw.get(d, 0))
        de = int(deaths_raw.get(d, 0))
        rcv = int(recovered_raw.get(d, 0))

        if prev_cases is None:
            new_c = 0
            new_d = 0
            new_r = 0
        else:
            new_c = max(0, c - prev_cases)
            new_d = max(0, de - prev_deaths)
            new_r = max(0, rcv - prev_recovered)

        prev_cases = c
        prev_deaths = de
        prev_recovered = rcv

        records.append(
            {
                "date": d,
                "cases_total": c,
                "deaths_total": de,
                "recovered_total": rcv,
                "cases_new": new_c,
                "deaths_new": new_d,
                "recovered_new": new_r,
            }
        )
    COVID_STORE.clear()
    COVID_STORE.extend(records)
    return records

def get_cached_covid_data():
    return list(COVID_STORE)

def plot_covid_graph(records):
    if not isinstance(records, list) or not records:
        return None
    try:
        date_objs = [datetime.strptime(r["date"], "%m/%d/%y") for r in records]
    except ValueError:
        date_objs = [datetime.fromisoformat(r["date"]) for r in records]

    cases = [r["cases_total"] for r in records]
    deaths = [r["deaths_total"] for r in records]
    recovered = [r["recovered_total"] for r in records]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(date_objs, cases, label="Cases")
    ax.plot(date_objs, deaths, label="Deaths")
    ax.plot(date_objs, recovered, label="Recovered")

    ax.set_xlabel("Date")
    ax.set_ylabel("Total")
    ax.set_title("COVID-19 Time Series")
    ax.legend()

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))   
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))     

    fig.autofmt_xdate(rotation=45)

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode("utf-8")



def save_covid_csv(records, csv_path):
    if not records:
        return {"error": "No records to save."}

    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            fieldnames = [
                "date",
                "cases_total",
                "deaths_total",
                "recovered_total",
                "cases_new",
                "deaths_new",
                "recovered_new",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                writer.writerow(
                    {
                        "date": r.get("date", ""),
                        "cases_total": r.get("cases_total", ""),
                        "deaths_total": r.get("deaths_total", ""),
                        "recovered_total": r.get("recovered_total", ""),
                        "cases_new": r.get("cases_new", ""),
                        "deaths_new": r.get("deaths_new", ""),
                        "recovered_new": r.get("recovered_new", ""),
                    }
                )
        return {"ok": True}
    except Exception as e:
        return {"error": f"Error saving CSV: {str(e)}."}
