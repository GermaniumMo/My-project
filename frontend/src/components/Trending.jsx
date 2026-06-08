function Trending({ topics, onTopicClick }) {
  const getTrendIcon = (trend) => {
    switch (trend) {
      case "up": return "📈";
      case "down": return "📉";
      default: return "📊";
    }
  };

  return (
    <aside className="trending">
      <div className="trending-card">
        <h3 className="trending-title">🔥 Trending Topics</h3>
        <div className="trending-list">
          {topics.map((topic) => (
            <button
              key={topic.tag}
              className="trending-item"
              onClick={() => onTopicClick(topic.tag)}
            >
              <span className="trending-tag">{topic.tag}</span>
              <span className="trending-stats">
                <span className="trending-count">{topic.count}</span>
                <span className="trending-icon">{getTrendIcon(topic.trend)}</span>
              </span>
            </button>
          ))}
        </div>
      </div>

      <div className="trending-card newsletter-card">
        <h3 className="trending-title">📬 Stay Updated</h3>
        <p className="newsletter-text">
          Get the latest AI breakthroughs delivered to your inbox weekly.
        </p>
        <div className="newsletter-form">
          <input
            type="email"
            placeholder="your@email.com"
            className="newsletter-input"
          />
          <button className="newsletter-btn">Subscribe</button>
        </div>
      </div>
    </aside>
  );
}

export default Trending;
