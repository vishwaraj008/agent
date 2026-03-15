Product Requirements Document (PRD)
1. Executive Summary

This project builds an AI-powered Business Intelligence Agent that answers founder-level questions using live data from monday.com boards.

The agent integrates with monday.com via GraphQL API, retrieves business data in real time, handles messy datasets, analyzes performance metrics, and returns actionable insights conversationally.

The system uses Google Gemini as the reasoning engine.

The agent will support queries such as:

How is our pipeline looking this quarter?

Which sector is generating the most revenue?

Which deals are stuck in negotiation?

Are we converting deals into work orders?

Which work orders are delayed?

The goal is to replace manual data analysis with an AI conversational BI assistant.

2. Objectives
Primary Goals

Build an AI agent capable of answering business intelligence questions

Integrate with monday.com boards using live API calls

Handle messy or inconsistent business data

Provide insightful answers instead of raw data

Maintain transparent tool/API call traces

3. Target Users
Founder / CEO

Needs quick answers about revenue, pipeline, and performance.

Sales Lead

Wants visibility into deal progression and conversion rates.

Operations Manager

Needs insights into work orders and delivery timelines.

4. Data Sources

Two monday.com boards will be used.

Deals Pipeline Board

Contains sales pipeline data.

Example fields:

Field	Description
Deal Name	Name of the deal
Owner Code	Salesperson
Client Code	Client identifier
Deal Status	Stage in pipeline
Close Date	Expected closing date
Work Orders Board

Contains operational delivery data.

Example fields:

Field	Description
Work Order Name	Project name
Execution Status	Work progress
Delivery Date	Expected delivery
Order Value	Revenue
5. Key Features
1 Conversational AI

Users can ask natural language questions.

Example:

How is our pipeline looking for the energy sector this quarter?
2 Live monday.com API Integration

Every user query triggers a live monday.com API call.

No caching or preloading.

Example GraphQL query:

query {
  boards(ids: BOARD_ID) {
    items_page {
      items {
        name
        column_values {
          text
          column {
            title
          }
        }
      }
    }
  }
}
3 Data Cleaning

Business data is messy.

The agent must normalize:

Missing values

Currency formats

Inconsistent labels

Date formats

Example cleaning logic:

₹1,20,000 → 120000
Energy Sector → energy
NULL → unknown
4 Business Intelligence

The agent must compute metrics such as:

Pipeline Health
Revenue by Sector
Conversion Rate
Delayed Orders
Deal Stage Distribution

5 Agent Tool Visibility

Every query should show tool usage.

Example:

Tool Call: Fetch Deals Data
Tool Call: Fetch Work Orders
Tool Call: Analyze Pipeline
6. System Architecture
User
  ↓
Frontend Chat UI
  ↓
Backend API
  ↓
AI Agent (Gemini)
  ↓
Monday API
  ↓
Data Cleaning
  ↓
Business Analysis
  ↓
Insight Response
7. Backend Architecture

The backend must follow this structure.

backend
│
├── main.py
│
├── routes
│   └── query_routes.py
│
├── controllers
│   └── query_controller.py
│
├── services
│   ├── ai_service.py
│   ├── monday_service.py
│   ├── analysis_service.py
│
├── utils
│   ├── data_cleaner.py
│   ├── logger.py
│
└── config
    └── settings.py
8. Component Responsibilities
main.py

Application entry point.

Responsibilities:

Initialize FastAPI

Register routes

Load environment variables

routes/

Defines API endpoints.

Example:

POST /query

Routes forward requests to controllers.

controllers/

Handles request validation.

Responsibilities:

Receive query

Validate input

Call services

Return response

services/

Contains core business logic.

monday_service

Fetch data from monday.com boards.

ai_service

Interact with Gemini LLM.

analysis_service

Generate business insights.

utils/

Helper utilities.

data_cleaner

Normalize messy datasets.

logger

Log agent actions and tool calls.

9. AI Agent Behavior

When a query is received:

Step 1

Understand the user question using Gemini.

Example:

Which sector has the highest pipeline value?
Step 2

Determine required data sources.

Possible sources:

Deals board

Work orders board

Both

Step 3

Call monday.com API.

Example:

Fetch Deals Board
Fetch Work Orders Board
Step 4

Normalize data.

Convert:

₹ values → numeric
NULL → default values
Mixed date formats → ISO
Step 5

Run analysis.

Examples:

Pipeline value
Deal conversion rate
Sector performance
Delayed orders

Step 6

Generate insights using Gemini.

Example response:

Energy sector pipeline is strong with ₹2.3M in active deals.
However, 70% of deals are still in early stages which may delay revenue realization.
10. Example Queries
How is our pipeline looking this quarter?

Which sector has the highest revenue?

Which deals are stuck in negotiation?

Are we converting deals into work orders?

Which work orders are delayed?

What is the average deal value by sector?
11. Environment Variables

Create .env.

# Gemini API
GEMINI_API_KEY=

# Monday API
MONDAY_API_KEY=

# Board IDs
DEALS_BOARD_ID=
WORK_ORDERS_BOARD_ID=

# App Settings
PORT=8000
ENV=development
12. Dependencies

Python packages:

fastapi
uvicorn
requests
pandas
python-dotenv
google-generativeai

Install with:

pip install fastapi uvicorn pandas requests python-dotenv google-generativeai
13. Deployment
Backend

Deploy using:

Render
Railway
Fly.io
Frontend

Deploy using:

Vercel
Netlify
14. Future Enhancements

Predictive analytics.

Examples:

Revenue forecasting

Deal probability scoring

Anomaly detection

Automated dashboards.

15. Success Metrics

System should:

Answer queries in <3 seconds

Handle inconsistent data gracefully

Provide meaningful business insights

Use live monday.com API calls