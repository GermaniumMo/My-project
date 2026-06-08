"""
AI News & Trends - FastAPI Backend
Serves AI news articles and trending topics via REST API.
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from news_fetcher import get_articles, TRENDING_TOPICS

app = FastAPI(
    title="AI News & Trends API",
    description="Aggregated AI news from top sources",
    version="1.0.0",
)

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "AI News & Trends API", "version": "1.0.0"}


@app.get("/api/news")
async def get_news(
    limit: int = Query(default=30, ge=1, le=100),
    source: str = Query(default=None, description="Filter by source name"),
    search: str = Query(default=None, description="Search in title/summary"),
    refresh: bool = Query(default=False, description="Force refresh cache"),
):
    """Get AI news articles, sorted by newest first."""
    articles = await get_articles(force_refresh=refresh)

    # Filter by source
    if source:
        articles = [
            a for a in articles
            if source.lower() in a.get("source", "").lower()
        ]

    # Search in title and summary
    if search:
        query = search.lower()
        articles = [
            a for a in articles
            if query in a.get("title", "").lower()
            or query in a.get("summary", "").lower()
        ]

    return {"articles": articles[:limit], "total": len(articles)}


@app.get("/api/trending")
async def get_trending():
    """Get trending AI topics with article counts."""
    return {"topics": TRENDING_TOPICS}


@app.get("/api/sources")
async def get_sources():
    """Get list of available news sources."""
    articles = await get_articles()
    sources = list({a["source"] for a in articles if a.get("source")})
    return {"sources": sorted(sources)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
