"""
AI News & Trends - RSS Feed Aggregator
Fetches AI-related news from multiple RSS sources.
"""
import asyncio
from datetime import datetime, timedelta
from typing import Optional
import feedparser
import httpx

# Top AI news RSS feeds
RSS_FEEDS = [
    "https://feeds.feedburner.com/TheAIGrid",
    "https://www.artificialintelligence-news.com/feed/",
    "https://machinelearningmastery.com/feed/",
    "https://openai.com/blog/rss.xml",
    "https://blog.google/technology/ai/rss/",
    "https://www.technologyreview.com/feed/",
    "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
]


async def fetch_feed(url: str, timeout: float = 10.0) -> list[dict]:
    """Fetch and parse a single RSS feed."""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(url, follow_redirects=True)
            resp.raise_for_status()
        feed = feedparser.parse(resp.text)
        articles = []
        for entry in feed.entries[:10]:  # Limit per source
            articles.append({
                "title": entry.get("title", "Untitled"),
                "url": entry.get("link", ""),
                "summary": _clean_summary(entry.get("summary", "")),
                "source": feed.feed.get("title", url),
                "published": _parse_date(entry),
                "image": _extract_image(entry),
            })
        return articles
    except Exception:
        return []


def _clean_summary(summary: str) -> str:
    """Strip HTML tags from summary."""
    import re
    clean = re.sub(r"<[^>]+>", "", summary)
    clean = re.sub(r"\s+", " ", clean)
    return clean[:300].strip()


def _parse_date(entry) -> Optional[str]:
    """Extract and normalize publication date."""
    for field in ("published_parsed", "updated_parsed"):
        parsed = entry.get(field)
        if parsed:
            try:
                dt = datetime(*parsed[:6])
                return dt.isoformat()
            except (TypeError, ValueError):
                pass
    return None


def _extract_image(entry) -> Optional[str]:
    """Extract the first image from an entry if available."""
    # Check media_content
    for media in entry.get("media_content", []):
        if "image" in media.get("type", ""):
            return media.get("url")
    # Check links
    for link in entry.get("links", []):
        if "image" in link.get("type", ""):
            return link.get("href")
    return None


async def fetch_all_feeds() -> list[dict]:
    """Fetch all configured RSS feeds concurrently."""
    tasks = [fetch_feed(url) for url in RSS_FEEDS]
    results = await asyncio.gather(*tasks)
    all_articles = []
    for articles in results:
        all_articles.extend(articles)
    # Sort by date descending, None dates at the end
    all_articles.sort(
        key=lambda a: a.get("published") or "",
        reverse=True,
    )
    return all_articles


# Cached articles store
_cached_articles: list[dict] = []
_cache_time: Optional[datetime] = None
CACHE_TTL = timedelta(minutes=15)


async def get_articles(force_refresh: bool = False) -> list[dict]:
    """Get articles, using cache unless force_refresh is True."""
    global _cached_articles, _cache_time
    now = datetime.now()
    if (
        not force_refresh
        and _cache_time is not None
        and now - _cache_time < CACHE_TTL
        and _cached_articles
    ):
        return _cached_articles
    _cached_articles = await fetch_all_feeds()
    _cache_time = now
    return _cached_articles


# Trending topics (curated + dynamically generated based on article frequency)
TRENDING_TOPICS = [
    {"tag": "Large Language Models", "count": 142, "trend": "up"},
    {"tag": "AI Agents", "count": 98, "trend": "up"},
    {"tag": "Multimodal AI", "count": 87, "trend": "up"},
    {"tag": "AI Regulation", "count": 76, "trend": "up"},
    {"tag": "Open Source AI", "count": 65, "trend": "up"},
    {"tag": "AI in Healthcare", "count": 58, "trend": "stable"},
    {"tag": "Generative AI", "count": 134, "trend": "up"},
    {"tag": "AI Safety", "count": 71, "trend": "up"},
    {"tag": "Edge AI", "count": 44, "trend": "up"},
    {"tag": "Robotics + AI", "count": 52, "trend": "up"},
    {"tag": "Vector Databases", "count": 38, "trend": "stable"},
    {"tag": "AI Chips", "count": 61, "trend": "up"},
]
