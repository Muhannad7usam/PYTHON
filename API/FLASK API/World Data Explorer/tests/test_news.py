import pytest
from app import news


class Response:
    def __init__(self, status_code=200, data=None, text=""):
        self.status_code = status_code
        self._data = data or {}
        self.text = text

    def json(self):
        return self._data


def test_get_news_data_success(monkeypatch):
    dummy_data = {
        "status": "ok",
        "totalResults": 2,
        "articles": [
            {
                "source": {"id": "src1", "name": "Source One"},
                "author": "Author 1",
                "title": "Title 1",
                "description": "Desc 1",
                "url": "http://example.com/1",
                "publishedAt": "2024-01-01T00:00:00Z",
            },
            {
                "source": {"id": None, "name": "Source Two"},
                "author": None,
                "title": "Title 2",
                "description": "Desc 2",
                "url": "http://example.com/2",
                "publishedAt": "2024-01-02T00:00:00Z",
            },
        ],
    }

    def fake_get(url, params=None, timeout=None):
        return Response(200, dummy_data)

    monkeypatch.setattr(news, "NEWS_API_KEY", "dummy-key")
    monkeypatch.setattr(news.requests, "get", fake_get)

    result = news.get_news_data("python")
    assert result["ok"] is True
    assert result["totalResults"] == 2
    assert len(result["articles"]) == 2


def test_get_news_data_http_error(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        return Response(500, {}, "error")

    monkeypatch.setattr(news, "NEWS_API_KEY", "dummy-key")
    monkeypatch.setattr(news.requests, "get", fake_get)

    result = news.get_news_data("python")
    assert "error" in result


def test_plot_news_by_source():
    articles = [
        {"source_name": "A"},
        {"source_name": "A"},
        {"source_name": "B"},
    ]
    img_b64 = news.plot_news_by_source(articles)
    assert isinstance(img_b64, str)
    assert img_b64 != ""


def test_save_news_csv(tmp_path):
    articles = [
        {
            "timestamp": "2024-01-01",
            "source_id": "src1",
            "source_name": "Source One",
            "author": "Author 1",
            "title": "Title 1",
            "description": "Desc 1",
            "url": "http://example.com/1",
            "published_at": "2024-01-01",
        }
    ]
    csv_path = tmp_path / "news.csv"
    result = news.save_news_csv(articles, str(csv_path))
    assert result == {"ok": True}
    assert csv_path.exists()
