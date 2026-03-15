import { useState } from 'react';

function ToolCallTrace({ toolCalls }) {
  const [expanded, setExpanded] = useState(false);

  if (!toolCalls || toolCalls.length === 0) return null;

  return (
    <div className="tool-calls">
      <button
        className={`tool-calls-toggle ${expanded ? 'expanded' : ''}`}
        onClick={() => setExpanded(!expanded)}
      >
        <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
          <path d="M4 2l4 4-4 4" />
        </svg>
        {toolCalls.length} Tool Call{toolCalls.length > 1 ? 's' : ''}
      </button>

      {expanded && (
        <div className="tool-calls-list">
          {toolCalls.map((tc, i) => (
            <span
              key={i}
              className={`tool-call-badge ${tc.status || 'success'}`}
            >
              <span className="tool-call-check">
                {tc.status === 'error' ? '✕' : tc.status === 'fallback' ? '⚠' : '✓'}
              </span>
              {tc.tool}: {tc.description}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function MetricsDisplay({ metrics }) {
  if (!metrics || Object.keys(metrics).length === 0) return null;

  const cards = [];
  if (metrics.pipeline) {
    cards.push({ value: metrics.pipeline.total_deals, label: 'Total Deals' });
    cards.push({ value: `₹${(metrics.pipeline.total_pipeline_value || 0).toLocaleString('en-IN')}`, label: 'Pipeline Value' });
  }
  if (metrics.conversion) {
    cards.push({ value: `${metrics.conversion.conversion_rate}%`, label: 'Conversion Rate' });
  }
  if (metrics.delayed_orders) {
    cards.push({ value: metrics.delayed_orders.delayed_count, label: 'Delayed Orders' });
  }

  if (cards.length === 0) return null;

  return (
    <div className="metrics-grid">
      {cards.map((card, i) => (
        <div key={i} className="metric-card">
          <div className="metric-value">{card.value}</div>
          <div className="metric-label">{card.label}</div>
        </div>
      ))}
    </div>
  );
}

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-ai'}`}>
      <div className={`message-avatar ${isUser ? 'message-avatar-user' : 'message-avatar-ai'}`}>
        {isUser ? '👤' : '🤖'}
      </div>
      <div className="message-content">
        <div className={`message-bubble ${isUser ? 'message-bubble-user' : 'message-bubble-ai'}`}>
          {isUser ? (
            message.content
          ) : (
            <>
              {message.content.split('\n').map((line, i) => (
                <p key={i}>{line}</p>
              ))}
              <MetricsDisplay metrics={message.metrics} />
            </>
          )}
        </div>
        {!isUser && message.toolCalls && (
          <ToolCallTrace toolCalls={message.toolCalls} />
        )}
        <span className="message-time">{message.time}</span>
      </div>
    </div>
  );
}
