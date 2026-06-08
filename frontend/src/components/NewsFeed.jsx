function NewsCard({ article }) {
  const timeAgo = (dateStr) => {
    if (!dateStr) return "";
    const diff = Date.now() - new Date(dateStr).getTime();
    const hours = Math.floor(diff / 3600000);
    if (hours < 1) return "Just now";
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    if (days < 7) return `${days}d ago`;
    return new Date(dateStr).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    });
  };

  return (
    <article className="news-card">
      <div className="news-card-content">
        <div className="news-card-meta">
          <span className="news-source">{article.source}</span>
          <span className="news-dot">·</span>
          <span className="news-time">{timeAgo(article.published)}</span>
        </div>
        <h3 className="news-title">
          <a href={article.url} target="_blank" rel="noopener noreferrer">
            {article.title}
          </a>
        </h3>
        {article.summary && (
          <p className="news-summary">{article.summary}</p>
        )}
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="news-read-more"
        >
          Read full article →
        </a>
      </div>
      {article.image && (
        <div className="news-card-image">
          <img src={article.image} alt="" loading="lazy" />
        </div>
      )}
    </article>
  );
}

function NewsFeed({ articles, loading, error, search }) {
  if (error) {
    return (
      <section className="news-feed">
        <div className="feed-error">
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
          <code>cd backend && python main.py</code>
        </div>
      </section>
    );
  }

  return (
    <section className="news-feed">
      <div className="feed-header">
        <h2>
          {search ? `Results for "${search}"` : "Latest AI News"}
        </h2>
        {articles.length > 0 && (
          <span className="feed-count">{articles.length} articles</span>
        )}
      </div>

      {loading ? (
        <div className="feed-loading">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="skeleton-card">
              <div className="skeleton-line skeleton-title" />
              <div className="skeleton-line skeleton-meta" />
              <div className="skeleton-line skeleton-body" />
              <div className="skeleton-line skeleton-body short" />
            </div>
          ))}
        </div>
      ) : articles.length === 0 ? (
        <div className="feed-empty">
          <span className="empty-icon">📭</span>
          <p>No articles found. Try a different search term.</p>
        </div>
      ) : (
        <div className="feed-list">
          {articles.map((article, i) => (
            <NewsCard key={article.url || i} article={article} />
          ))}
        </div>
      )}
    </section>
  );
}

export default NewsFeed;
