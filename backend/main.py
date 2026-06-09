"""
AI News & Trends - FastAPI Backend
Serves AI news articles and trending topics via REST API.
Also includes outfit roast endpoint.
"""
import os
import base64
import httpx
from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from news_fetcher import get_articles, TRENDING_TOPICS

app = FastAPI(
    title="AI News & Trends API",
    description="Aggregated AI news from top sources",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read API key from file (keeps it out of source control)
def _read_api_key():
    key_file = os.path.join(os.path.dirname(__file__), ".apikey")
    if os.path.exists(key_file):
        with open(key_file) as f:
            return f.read().strip()
    return os.getenv("OPENROUTER_API_KEY", "")

OPENROUTER_API_KEY = _read_api_key()
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
ROAST_MODEL = "google/gemma-4-26b-a4b-it:free"

ROAST_PROMPT_IMAGE = """You are a savage fashion critic with the wit of a comedy roast master.
You're looking at someone's outfit photo. Your job is to ROAST their outfit - be brutally honest, hilarious, and creative.

Rules:
- Start with a fire score out of 10 (1 = fashion disaster, 10 = actually slayed)
- Then deliver 3-5 savage observations about their outfit
- Be specific - mention actual clothing items, colors, fit, style choices
- Use comedy roast style humor: exaggerate, use metaphors, be playful but NOT mean-spirited
- End with a backhanded compliment or genuinely encouraging note
- Don't mention that you're an AI
- Keep it under 200 words
- Format your response in plain text, no markdown"""

ROAST_PROMPT_TEXT = """You are a savage fashion critic with the wit of a comedy roast master.
Someone described their outfit to you. Your job is to ROAST it - be brutally honest, hilarious, and creative.

Rules:
- Start with a fire score out of 10 (1 = fashion disaster, 10 = actually slayed)
- Then deliver 3-5 savage observations based on their description
- Use comedy roast style humor: exaggerate, use metaphors, be playful but NOT mean-spirited
- End with a backhanded compliment or genuinely encouraging note
- Keep it under 200 words
- Format your response in plain text, no markdown"""


class RoastRequest(BaseModel):
    image_base64: Optional[str] = None
    mime_type: str = "image/jpeg"
    description: Optional[str] = None


@app.post("/api/roast")
async def roast_outfit(req: RoastRequest):
    """Proxy to OpenRouter to roast an outfit (image or text description)."""
    try:
        # Build the message content
        if req.image_base64:
            content = [
                {"type": "text", "text": ROAST_PROMPT_IMAGE},
                {"type": "image_url", "image_url": {"url": f"data:{req.mime_type};base64,{req.image_base64}"}}
            ]
        else:
            content = [
                {"type": "text", "text": ROAST_PROMPT_TEXT},
                {"type": "text", "text": f"Here's what the person is wearing: {req.description or 'unknown outfit'}. Roast this outfit."}
            ]

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                OPENROUTER_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "Outfit Roaster",
                },
                json={
                    "model": ROAST_MODEL,
                    "messages": [{"role": "user", "content": content}],
                    "max_tokens": 500,
                    "temperature": 0.9,
                },
            )

            if resp.status_code != 200:
                detail = resp.text
                try:
                    detail = resp.json().get("error", {}).get("message", detail)
                except Exception:
                    pass
                raise HTTPException(status_code=resp.status_code, detail=f"OpenRouter error: {detail}")

            data = resp.json()
            roast = data["choices"][0]["message"]["content"]
            return {"roast": roast}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

    if source:
        articles = [
            a for a in articles
            if source.lower() in a.get("source", "").lower()
        ]

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
