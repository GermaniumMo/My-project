function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-brand">
          <span className="logo-icon">⟐</span>
          <span>AI<span className="logo-highlight">Pulse</span></span>
        </div>
        <p className="footer-tagline">
          Aggregating AI news from the world's leading sources. Stay informed, stay ahead.
        </p>
        <div className="footer-links">
          <span>Built with React + FastAPI</span>
          <span className="footer-dot">·</span>
          <span>© {new Date().getFullYear()} AIPulse</span>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
