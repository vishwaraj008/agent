# AI Business Intelligence Agent

A full-stack, AI-powered Business Intelligence agent that bridges the gap between raw CRM data (from monday.com) and actionable insights using Google's Gemini LLM. 

Designed for founders, sales leads, and operations managers, it directly answers complex queries about pipeline health, conversion rates, and operations in a conversational interface.

## Features

- **Live Data Integration:** Fetches real-time data from monday.com (Deals Pipeline & Work Orders boards) using GraphQL.
- **Intelligent Intent Detection:** Uses Gemini 2.5 Flash to automatically interpret exactly what data and analysis type your query needs.
- **Automated Data Cleaning & Analysis:** Processes messy board data, handling missing values, currencies, and dates, and calculates KPIs (Conversion Rate, Pipeline Value, Delayed Orders).
- **Conversational Insights:** Translates raw numbers into professional, readable summaries that quickly highlight bottlenecks or opportunities.
- **Professional Chat Interface:** A premium, dark-themed UI built in React (Vite) integrating glass-morphism and readable tool execution traces.
- **Radical Transparency:** Shows the exact internal "tool calls" (e.g., Data Fetching → Analysis → Insight Generation) beneath every response.

## Tech Stack

**Backend**
- Python 3.12+
- FastAPI & Uvicorn (RESTful Application)
- Google GenAI SDK (Gemini 2.5 Flash via REST transport)
- Pytest (37/37 passing test suite)

**Frontend**
- React (bootstrapped with Vite)
- Vanilla CSS (Stitch MCP generated premium dark theme)

## Project Structure

```text
├── backend/
│   ├── main.py                    # FastAPI entrypoint
│   ├── config/settings.py         # Environment variables & API validation
│   ├── routes/query_routes.py     # API Endpoints (/api/query, /api/health)
│   ├── controllers/               # Route controllers & Pydantic models
│   ├── services/
│   │   ├── ai_service.py          # Gemini LLM orchestration
│   │   ├── monday_service.py      # GraphQL queries to monday.com
│   │   └── analysis_service.py    # Business logic & KPI computation
│   ├── utils/
│   │   ├── data_cleaner.py        # Normalizes dates, currencies, and text
│   │   └── logger.py              # Structured logging and tool traces
│   └── tests/                     # Comprehensive Pytest suite
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx                # Main application hub
│       ├── App.css                # Design system styling
│       ├── components/            # Sidebar, Header, ChatInput, MessageBubbles
│       └── services/api.js        # Axios wrapper to talk to backend
└── .gitignore                     # Ignore configs
```

## Setup & Installation

### Prerequisites
- Python 3.12+
- Node.js v18+ & npm
- Monday.com API Token and Board IDs (Deals & Work Orders)
- Google Gemini API Key

### 1. Backend Setup

```bash
cd backend

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure your environment
cp .env.example .env
```

Open `backend/.env` and fill in your actual credentials:
```env
GEMINI_API_KEY="your-gemini-key"
MONDAY_API_KEY="your-monday-token"
DEALS_BOARD_ID="your-deals-board-id"
WORK_ORDERS_BOARD_ID="your-work-orders-board-id"
PORT=8000
ENV=development
```

Start the backend server:
```bash
python3 -m uvicorn main:app --reload --port 8000
```
*(The backend will run on http://localhost:8000)*

### 2. Frontend Setup

Open a **new terminal tab**:

```bash
cd frontend

# Install Node modules
npm build
npm install

# Start the development server
npm run dev
```
*(The frontend will run on http://localhost:5173)*

## Usage

Once both servers are running, map your browser to [`http://localhost:5173`](http://localhost:5173). 

You'll see the welcome screen. Try asking queries like:
- *"How is our pipeline looking this quarter?"*
- *"Which sector generates the most revenue?"*
- *"Are we converting deals into orders efficiently?"*
- *"Which deals are currently delayed or stuck?"*

Click on **`[▸ Tool Calls]`** under any AI response to inspect exactly how the AI routed your request, fetched the required data, and generated its analysis.

## Testing

To run the full backend testing suite (Data cleaners, API endpoints, Analysis services):

```bash
cd backend
python3 -m pytest tests/ -v
```
