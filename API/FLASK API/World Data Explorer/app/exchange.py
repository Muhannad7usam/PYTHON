import os
import io
import csv
import base64
import requests

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
EXCHANGE_URL = "https://api.exchangerate.host/live"

EXCHANGE_STORE = []


def get_exchange_data(base="USD", symbols=None, timeout=20):
    params = {
        "access_key": EXCHANGE_API_KEY,
        "source": base,
    }
    if symbols:
        params["currencies"] = symbols

    try:
        r = requests.get(EXCHANGE_URL, params=params, timeout=timeout)
    except Exception as e:
        return {"error": f"Error connecting to exchange API: {str(e)}."}

    if r.status_code != 200:
        return {
            "error": f"Exchange API returned HTTP {r.status_code}.",
            "message": r.text[:500],
        }

    data = r.json() or {}
    if not data.get("success", False):
        return {"error": str(data.get("error", {}).get("info", "Unknown error"))}

    source = data.get("source", base)
    ts = data.get("timestamp")
    quotes = data.get("quotes") or {}

    records = []
    for pair, rate in quotes.items():
        if not pair.startswith(source):
            continue
        code = pair[len(source):]
        try:
            rate_val = float(rate)
        except Exception:
            continue
        inverse = 1.0 / rate_val if rate_val else None
        records.append(
            {
                "timestamp": ts,
                "base": source,
                "code": code,
                "pair": f"{source}:{code}",
                "rate": rate_val,
                "inverse": inverse,
            }
        )

    records.sort(key=lambda r: r["code"])

    EXCHANGE_STORE.clear()
    EXCHANGE_STORE.extend(records)

    return records


def get_cached_exchange_data():
    return list(EXCHANGE_STORE)


def plot_exchange_bar(records):
    if not records:
        return None

    codes = [r["code"] for r in records]
    rates = [r["rate"] for r in records]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(codes, rates)
    ax.set_xlabel("Currency")
    ax.set_ylabel("Rate")
    ax.set_title(f"Exchange Rates ({records[0]['base']} base)")

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode("utf-8")


def save_exchange_csv(records, csv_path):
    if not records:
        return {"error": "No records to save."}

    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            fieldnames = ["timestamp", "base", "code", "pair", "rate", "inverse"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                writer.writerow(
                    {
                        "timestamp": r.get("timestamp", ""),
                        "base": r.get("base", ""),
                        "code": r.get("code", ""),
                        "pair": r.get("pair", ""),
                        "rate": r.get("rate", ""),
                        "inverse": r.get("inverse", ""),
                    }
                )
        return {"ok": True}
    except Exception as e:
        return {"error": f"Error saving CSV: {str(e)}."}
