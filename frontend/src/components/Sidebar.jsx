export default function Sidebar({ chatHistory, onNewChat }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">🧠</div>
        <div>
          <div className="sidebar-logo-text">BI Agent</div>
          <div className="sidebar-logo-sub">AI Intelligence</div>
        </div>
      </div>

      <button className="new-chat-btn" onClick={onNewChat}>
        <span>+</span> New Chat
      </button>

      <div className="sidebar-section-title">Navigation</div>
      <nav className="sidebar-nav">
        <button className="sidebar-nav-item active">
          💬 Chat
        </button>
      </nav>

      <div className="sidebar-section-title">Recent Chats</div>
      <div className="chat-history">
        {chatHistory.map((chat, i) => (
          <div key={i} className="chat-history-item">
            💭 {chat}
          </div>
        ))}
      </div>

      <div className="sidebar-footer">
        <button className="sidebar-nav-item">
          ⚙️ Settings
        </button>
      </div>
    </aside>
  );
}
