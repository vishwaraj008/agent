const API_BASE = 'http://localhost:8000/api';

export async function sendQuery(question) {
  const response = await fetch(`${API_BASE}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Network error' }));
    throw new Error(error.detail || 'Failed to process query');
  }

  return response.json();
}

export async function healthCheck() {
  const response = await fetch(`${API_BASE}/health`);
  return response.json();
}
