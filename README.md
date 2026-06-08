# AIPulse — AI News & Trends

> Real-time AI news aggregation platform. Stay ahead with curated breakthroughs, industry trends, and research — from the world's leading sources.

![Tech Stack](https://img.shields.io/badge/frontend-React_19-61DAFB?logo=react)
![Tech Stack](https://img.shields.io/badge/build-Vite-646CFF?logo=vite)
![Tech Stack](https://img.shields.io/badge/backend-FastAPI-009688?logo=fastapi)
![Tech Stack](https://img.shields.io/badge/runtime-Python_3.11-3776AB?logo=python)

## Features

- **📡 Live RSS Aggregation** — Fetches AI news from 7+ top sources (OpenAI, MIT Tech Review, Google AI, ML Mastery, and more)
- **🔥 Trending Topics** — Curated list of what's hot in AI right now
- **🔍 Full-Text Search** — Search across all articles by keyword
- **🎨 Modern Dark Theme** — Glassmorphism UI with animated gradient backgrounds
- **📱 Fully Responsive** — Works great on desktop, tablet, and mobile
- **⚡ Real-Time** — 15-minute article cache with on-demand refresh

## Project Structure

```
my-project/
├── backend/
│   ├── main.py              # FastAPI server (REST API)
│   ├── news_fetcher.py      # RSS feed aggregation logic
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Root component with state management
│   │   ├── index.css        # Full dark theme stylesheet
│   │   ├── main.jsx         # React entry point
│   │   └── components/
│   │       ├── Navbar.jsx   # Sticky nav with search
│   │       ├── Hero.jsx     # Animated hero section
│   │       ├── NewsFeed.jsx # Article list with loading skeletons
│   │       ├── Trending.jsx # Trending topics sidebar
│   │       └── Footer.jsx   # Site footer
│   ├── index.html           # HTML shell with Inter font
│   └── package.json         # Node.js dependencies
├── .gitignore
└── README.md
```

## Quick Start

### 1. Backend (API Server)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

API runs on **http://localhost:8000**

| Endpoint | Description |
|----------|-------------|
| `GET /` | Health check |
| `GET /api/news?limit=30&search=...&source=...` | News articles |
| `GET /api/trending` | Trending topics |
| `GET /api/sources` | Available news sources |

### 2. Frontend (Dev Server)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on **http://localhost:5173**

### 3. Production Build

```bash
cd frontend
npm run build        # Outputs to frontend/dist/
```

Then serve the `dist/` folder with any static server (nginx, `python -m http.server`, etc.) pointing API calls to the backend.

## API Examples

```bash
# Get latest news
curl http://localhost:8000/api/news

# Search for "agents"
curl "http://localhost:8000/api/news?search=agents"

# Force fresh fetch
curl "http://localhost:8000/api/news?refresh=true"

# Get trending topics
curl http://localhost:8000/api/trending
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19 + Vite |
| **Backend** | Python FastAPI + Uvicorn |
| **RSS Parsing** | feedparser + httpx (async) |
| **Styling** | Custom CSS (CSS Custom Properties, Glassmorphism, CSS Animations) |
| **Fonts** | Inter (Google Fonts) |

## News Sources

- OpenAI Blog
- Google AI Blog
- MIT Technology Review
- Machine Learning Mastery
- Artificial Intelligence News
- The AI Grid
- ScienceDaily AI

## License

MIT
