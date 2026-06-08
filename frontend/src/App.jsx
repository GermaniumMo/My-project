import { useState, useEffect, useCallback } from "react";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import NewsFeed from "./components/NewsFeed";
import Trending from "./components/Trending";
import Footer from "./components/Footer";

const API_BASE = "http://localhost:8000";

function App() {
  const [articles, setArticles] = useState([]);
  const [trending, setTrending] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [error, setError] = useState(null);

  const fetchArticles = useCallback(async (query = "") => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({ limit: "50" });
      if (query) params.set("search", query);
      const res = await fetch(`${API_BASE}/api/news?${params}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setArticles(data.articles);
    } catch (err) {
      setError("Failed to load news. Is the backend running on :8000?");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchTrending = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/trending`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setTrending(data.topics);
    } catch {
      // trending is non-critical
    }
  }, []);

  useEffect(() => {
    fetchArticles();
    fetchTrending();
  }, [fetchArticles, fetchTrending]);

  const handleSearch = (query) => {
    setSearch(query);
    fetchArticles(query);
  };

  return (
    <div className="app">
      <Navbar onSearch={handleSearch} />
      <Hero />
      <main className="main-content">
        <NewsFeed
          articles={articles}
          loading={loading}
          error={error}
          search={search}
        />
        <Trending topics={trending} onTopicClick={handleSearch} />
      </main>
      <Footer />
    </div>
  );
}

export default App;
