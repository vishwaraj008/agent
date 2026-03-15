import { useState } from 'react';

export default function ChatInput({ onSend, isLoading }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    onSend(trimmed);
    setInput('');
  };

  return (
    <div className="input-bar">
      <form className="input-bar-inner" onSubmit={handleSubmit}>
        <input
          id="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your business data..."
          disabled={isLoading}
          autoComplete="off"
        />
        <button
          type="submit"
          className="send-btn"
          disabled={!input.trim() || isLoading}
          aria-label="Send message"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M22 2L11 13" />
            <path d="M22 2L15 22L11 13L2 9L22 2Z" />
          </svg>
        </button>
      </form>
      <div className="input-hint">
        BI Agent can make mistakes. Consider verifying important metrics.
      </div>
    </div>
  );
}
