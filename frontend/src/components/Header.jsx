export default function Header({ isConnected }) {
  return (
    <header className="header">
      <h1 className="header-title">AI Business Intelligence Assistant</h1>
      <div className="header-status">
        <div className={`status-dot ${!isConnected ? 'disconnected' : ''}`}
             style={!isConnected ? { background: 'var(--error)', boxShadow: '0 0 8px rgba(239,68,68,0.5)' } : {}} />
        <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
      </div>
    </header>
  );
}
