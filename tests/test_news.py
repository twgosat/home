from datetime import datetime, timedelta, timezone

from cuanlens.models import NewsItem
from cuanlens.news import clean_news, sentiment_hint
from cuanlens.providers.yahoo import parse_news

NOW = datetime(2026, 10, 12, tzinfo=timezone.utc)


def item(title, days_ago=1, **kw):
    return NewsItem(title=title, published=NOW - timedelta(days=days_ago), **kw)


def test_dedupes_ignoring_case_and_punctuation():
    out = clean_news([item("Laba BBCA naik!"), item("laba bbca  naik")], now=NOW)
    assert len(out) == 1


def test_drops_old_and_empty_and_sorts_newest_first():
    out = clean_news([item("lama", 90), item("   "), item("b", 5), item("a", 1)], now=NOW)
    assert [n.title for n in out] == ["a", "b"]


def test_strips_html_and_truncates_summary():
    out = clean_news([item("t", summary="<p>" + "x" * 500 + "</p>")], summary_chars=50, now=NOW)
    assert "<" not in out[0].summary and len(out[0].summary) == 50 and out[0].summary.endswith("…")


def test_naive_datetimes_are_accepted():
    naive = NewsItem(title="x", published=datetime(2026, 10, 10))
    assert clean_news([naive], now=NOW)[0].published.tzinfo is not None


def test_undated_kept_after_dated():
    out = clean_news([NewsItem(title="undated"), item("dated")], now=NOW)
    assert [n.title for n in out] == ["dated", "undated"]


def test_max_items():
    assert len(clean_news([item(f"n{i}") for i in range(20)], max_items=3, now=NOW)) == 3


def test_sentiment_hint():
    assert sentiment_hint("Laba melonjak, rekor dividen") == "positif"
    assert sentiment_hint("Saham anjlok setelah gugatan") == "negatif"
    assert sentiment_hint("RUPS digelar Selasa") == "netral"


def test_parse_news_new_and_legacy_layouts():
    new = {
        "content": {
            "title": "Baru",
            "summary": "ringkas",
            "provider": {"displayName": "Reuters"},
            "pubDate": "2026-10-11T08:00:00Z",
            "canonicalUrl": {"url": "https://x/1"},
        }
    }
    old = {"title": "Lama", "publisher": "CNBC", "providerPublishTime": 1760000000, "link": "https://x/2"}
    junk = ["not a dict", {"content": {"title": ""}}]
    items = parse_news([new, old, *junk])
    assert [(n.title, n.publisher, n.url) for n in items] == [
        ("Baru", "Reuters", "https://x/1"),
        ("Lama", "CNBC", "https://x/2"),
    ]
    assert all(n.published is not None and n.published.tzinfo for n in items)
    assert parse_news(None) == []
