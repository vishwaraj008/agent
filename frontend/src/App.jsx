import { useState, useRef, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import WelcomeScreen from './components/WelcomeScreen';
import MessageBubble from './components/MessageBubble';
import ChatInput from './components/ChatInput';
import { sendQuery, healthCheck } from './services/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const chatEndRef = useRef(null);

  // Check backend health on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const health = await healthCheck();
        setIsConnected(health.status === 'healthy');
      } catch {
        setIsConnected(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const formatTime = () => {
    return new Date().toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const handleSendMessage = async (question) => {
    // Add user message
    const userMessage = {
      role: 'user',
      content: question,
      time: formatTime(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendQuery(question);

      const aiMessage = {
        role: 'ai',
        content: response.answer,
        toolCalls: response.tool_calls,
        metrics: response.metrics,
        time: formatTime(),
      };
      setMessages((prev) => [...prev, aiMessage]);

      // Add to chat history
      const shortQuestion = question.length > 35 ? question.slice(0, 35) + '...' : question;
      setChatHistory((prev) => {
        const updated = [shortQuestion, ...prev];
        return updated.slice(0, 10); // Keep last 10
      });
    } catch (error) {
      const errorMessage = {
        role: 'ai',
        content: `Sorry, I encountered an error: ${error.message}. Please check that the backend server is running on port 8000.`,
        toolCalls: [{ tool: 'Error', description: error.message, status: 'error' }],
        time: formatTime(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
  };

  const showWelcome = messages.length === 0;

  return (
    <div className="app-layout">
      <Sidebar chatHistory={chatHistory} onNewChat={handleNewChat} />

      <main className="main-content">
        <Header isConnected={isConnected} />

        <div className="chat-area">
          {showWelcome ? (
            <WelcomeScreen onSuggestionClick={handleSendMessage} />
          ) : (
            <>
              {messages.map((msg, i) => (
                <MessageBubble key={i} message={msg} />
              ))}

              {isLoading && (
                <div className="loading-message">
                  <div className="message-avatar message-avatar-ai">🤖</div>
                  <div className="loading-dots">
                    <div className="loading-dot" />
                    <div className="loading-dot" />
                    <div className="loading-dot" />
                  </div>
                </div>
              )}

              <div ref={chatEndRef} />
            </>
          )}
        </div>

        <ChatInput onSend={handleSendMessage} isLoading={isLoading} />
      </main>
    </div>
  );
}

export default App;
