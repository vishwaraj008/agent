const SUGGESTIONS = [
  { icon: '📊', text: 'How is our pipeline looking this quarter?' },
  { icon: '💰', text: 'Which sector generates the most revenue?' },
  { icon: '📋', text: 'Which deals are stuck in negotiation?' },
  { icon: '⚡', text: 'Are we converting deals into work orders?' },
];

export default function WelcomeScreen({ onSuggestionClick }) {
  return (
    <div className="welcome-container">
      <div className="welcome-icon">🧠</div>
      <h2 className="welcome-title">What would you like to know about your business?</h2>
      <p className="welcome-subtitle">
        Ask questions about your deals, pipeline, revenue, and operations. I'll fetch live data and provide actionable insights.
      </p>
      <div className="suggestion-grid">
        {SUGGESTIONS.map((s, i) => (
          <div key={i} className="suggestion-card" onClick={() => onSuggestionClick(s.text)}>
            <span className="suggestion-card-icon">{s.icon}</span>
            <span className="suggestion-card-text">{s.text}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
