import os
import io
import csv
import base64
from datetime import datetime
import requests

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_URL = "https://newsapi.org/v2/everything"

NEWS_STORE = []


def get_news_data(
    q,
    from_date=None,
    to_date=None,
    language=None,
    sort_by="publishedAt",
    page_size=80,
    page=1,
    timeout=20,
):
    if not NEWS_API_KEY:
        return {"error": "NEWS_API_KEY is not set."}

    params = {
        "q": q,
        "sortBy": sort_by,
        "pageSize": page_size,
        "page": page,
        "apiKey": NEWS_API_KEY,
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if language:
        params["language"] = language

    try:
        r = requests.get(NEWS_URL, params=params, timeout=timeout)
    except Exception as e:
        return {"error": f"Error connecting to News API: {str(e)}."}

    if r.status_code != 200:
        return {
            "error": f"There is no data found for these requirements.",
            "message": r.text[:500],
        }

    data = r.json() or {}
    if data.get("status") != "ok":
        return {"error": str(data.get("message", "Unknown error"))}

    articles_raw = data.get("articles") or []
    articles = []

    for a in articles_raw:
        source = a.get("source") or {}
        published_at = a.get("publishedAt")
        try:
            ts = (
                datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                if published_at
                else None
            )
        except Exception:
            ts = None

        articles.append(
            {
                "timestamp": ts.isoformat() if ts else "",
                "source_id": source.get("id"),
                "source_name": source.get("name"),
                "author": a.get("author"),
                "title": a.get("title"),
                "description": a.get("description"),
                "url": a.get("url"),
                "published_at": published_at or "",
            }
        )

    NEWS_STORE.clear()
    NEWS_STORE.extend(articles)

    return {"ok": True, "totalResults": data.get("totalResults", 0), "articles": articles}


def get_cached_news():
    return list(NEWS_STORE)


def plot_news_by_source(articles):
    if not articles:
        return None

    counts = {}
    for a in articles:
        name = a.get("source_name") or "Unknown"
        counts[name] = counts.get(name, 0) + 1

    labels = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values)
    ax.set_xlabel("Source")
    ax.set_ylabel("Articles")
    ax.set_title("Articles per News Source")
    ax.tick_params(axis="x", labelrotation=45)

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)

    return base64.b64encode(buf.getvalue()).decode("utf-8")


def save_news_csv(articles, csv_path):
    if not articles:
        return {"error": "No articles to save."}

    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            fieldnames = [
                "timestamp",
                "source_id",
                "source_name",
                "author",
                "title",
                "description",
                "url",
                "published_at",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for a in articles:
                writer.writerow(
                    {
                        "timestamp": a.get("timestamp", ""),
                        "source_id": a.get("source_id", ""),
                        "source_name": a.get("source_name", ""),
                        "author": a.get("author", ""),
                        "title": a.get("title", ""),
                        "description": a.get("description", ""),
                        "url": a.get("url", ""),
                        "published_at": a.get("published_at", ""),
                    }
                )
        return {"ok": True}
    except Exception as e:
        return {"error": f"Error saving CSV: {str(e)}."}
