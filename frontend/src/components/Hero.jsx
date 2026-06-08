function Hero() {
  return (
    <section className="hero">
      <div className="hero-bg">
        <div className="hero-orb orb-1" />
        <div className="hero-orb orb-2" />
        <div className="hero-orb orb-3" />
      </div>
      <div className="hero-content">
        <span className="hero-badge">🔥 Trending Now</span>
        <h1 className="hero-title">
          The Future of{" "}
          <span className="hero-gradient">Artificial Intelligence</span>
        </h1>
        <p className="hero-subtitle">
          Stay ahead with real-time AI news, breakthroughs, and industry trends — 
          curated from the world's leading sources.
        </p>
      </div>
    </section>
  );
}

export default Hero;
