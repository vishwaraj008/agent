"""
AI Service — Gemini-powered query processing with tool orchestration.
Understands user questions, fetches relevant data, runs analysis,
and generates insightful responses.
"""

import json
import asyncio
import google.generativeai as genai
from config.settings import settings
from services import monday_service, analysis_service
from utils.logger import logger, ToolCallTracker


# Configure Gemini with REST transport to avoid gRPC DNS issues
if settings.GEMINI_API_KEY:
    genai.configure(
        api_key=settings.GEMINI_API_KEY,
        transport="rest",
    )


INTENT_PROMPT = """You are a business intelligence assistant. Analyze the user's question and determine:
1. What data sources are needed: "deals", "work_orders", or "both"
2. What type of analysis is needed: "pipeline", "revenue", "conversion", "delayed", "general"

Respond ONLY with valid JSON like:
{"data_sources": "both", "analysis_type": "general"}

User question: {question}"""


INSIGHT_PROMPT = """You are an AI Business Intelligence assistant for a company.
You help founders, sales leads, and operations managers understand their business data.

Given the following business data analysis results, provide a clear, insightful, and actionable response
to the user's question. Be conversational but professional. Use specific numbers where available.
Format currency in Indian Rupees (₹) with proper formatting.

User Question: {question}

Analysis Results:
{analysis}

Provide a clear, concise insight in 3-5 sentences. Do NOT include raw JSON. Speak naturally as a business advisor would."""


GEMINI_TIMEOUT = 30  # seconds


def _extract_summaries(metrics: dict) -> str:
    """Extract only the summary strings from metrics to keep the Gemini payload small."""
    summaries = []
    for key, value in metrics.items():
        if isinstance(value, dict):
            if "summary" in value:
                summaries.append(f"**{key.replace('_', ' ').title()}**: {value['summary']}")
            # Include key numeric values
            for sub_key in ["total_deals", "total_pipeline_value", "conversion_rate",
                            "delayed_count", "total_orders", "total_work_orders"]:
                if sub_key in value:
                    summaries.append(f"  - {sub_key.replace('_', ' ').title()}: {value[sub_key]}")
            # Include stage distribution if present
            if "stages" in value and isinstance(value["stages"], dict):
                stages_str = ", ".join(f"{k}: {v}" for k, v in value["stages"].items())
                summaries.append(f"  - Stage Distribution: {stages_str}")
            # Include top sectors if present
            if "sectors" in value and isinstance(value["sectors"], dict):
                top_sectors = sorted(value["sectors"].items(),
                                     key=lambda x: x[1].get("value", 0) if isinstance(x[1], dict) else 0,
                                     reverse=True)[:5]
                sectors_str = ", ".join(
                    f"{k} (₹{v.get('value', 0):,.0f}, {v.get('count', 0)} deals)"
                    for k, v in top_sectors if isinstance(v, dict)
                )
                if sectors_str:
                    summaries.append(f"  - Top Sectors: {sectors_str}")
            # Include delayed orders list if present
            if "delayed_orders" in value and isinstance(value["delayed_orders"], list):
                for order in value["delayed_orders"][:5]:
                    summaries.append(f"  - Delayed: {order.get('name', '?')} (due: {order.get('delivery_date', '?')}, status: {order.get('status', '?')})")
    return "\n".join(summaries) if summaries else json.dumps(metrics, indent=2, default=str)


async def process_query(question: str) -> dict:
    """
    Process a user's business intelligence query end-to-end.

    Steps:
    1. Understand intent via Gemini
    2. Fetch relevant data from monday.com
    3. Run BI analysis
    4. Generate insight via Gemini
    5. Return response with tool call trace
    """
    tracker = ToolCallTracker()

    try:
        # Step 1: Understand intent
        tracker.record("Understand Query", f"Analyzing question: '{question[:80]}...'")
        intent = await _determine_intent(question, tracker)
        data_sources = intent.get("data_sources", "both")
        analysis_type = intent.get("analysis_type", "general")

        # Step 2: Fetch data
        deals = []
        work_orders = []

        if data_sources in ("deals", "both"):
            tracker.record("Fetch Deals Data", "Querying monday.com Deals Pipeline board")
            try:
                deals = await asyncio.to_thread(monday_service.fetch_deals)
                tracker.record("Fetch Deals Data", f"Retrieved {len(deals)} deals", "success")
            except Exception as e:
                tracker.record("Fetch Deals Data", str(e), "error")

        if data_sources in ("work_orders", "both"):
            tracker.record("Fetch Work Orders", "Querying monday.com Work Orders board")
            try:
                work_orders = await asyncio.to_thread(monday_service.fetch_work_orders)
                tracker.record("Fetch Work Orders", f"Retrieved {len(work_orders)} work orders", "success")
            except Exception as e:
                tracker.record("Fetch Work Orders", str(e), "error")

        # Step 3: Run analysis
        tracker.record("Analyze Data", f"Running {analysis_type} analysis")
        metrics = _run_analysis(deals, work_orders, analysis_type)
        tracker.record("Analyze Data", "Analysis completed", "success")

        # Step 4: Generate insight
        tracker.record("Generate Insight", "Creating AI-powered business insight")
        answer = await _generate_insight(question, metrics, tracker)

        return {
            "answer": answer,
            "tool_calls": tracker.get_trace(),
            "metrics": metrics,
        }

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        tracker.record("Error", str(e), "error")
        return {
            "answer": f"I encountered an issue while processing your question. Please ensure your API keys are configured correctly. Error: {str(e)}",
            "tool_calls": tracker.get_trace(),
            "metrics": {},
        }


async def _determine_intent(question: str, tracker: ToolCallTracker) -> dict:
    """Use Gemini to determine what data and analysis the question requires."""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Run in thread to avoid blocking the event loop
        response = await asyncio.wait_for(
            asyncio.to_thread(model.generate_content, INTENT_PROMPT.format(question=question)),
            timeout=GEMINI_TIMEOUT,
        )
        text = response.text.strip()

        # Extract JSON from response (handle markdown code blocks)
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        intent = json.loads(text)
        tracker.record("Understand Query", f"Intent: sources={intent.get('data_sources')}, analysis={intent.get('analysis_type')}", "success")
        return intent

    except asyncio.TimeoutError:
        logger.warning("Intent detection timed out, defaulting to 'both/general'")
        tracker.record("Understand Query", "Timed out, defaulting to fetch all data", "fallback")
        return {"data_sources": "both", "analysis_type": "general"}
    except Exception as e:
        logger.warning(f"Intent detection failed, defaulting to 'both/general': {e}")
        tracker.record("Understand Query", "Defaulting to fetch all data", "fallback")
        return {"data_sources": "both", "analysis_type": "general"}


def _run_analysis(deals: list[dict], work_orders: list[dict], analysis_type: str) -> dict:
    """Run the appropriate analysis based on intent."""
    if analysis_type == "pipeline":
        return {"pipeline": analysis_service.analyze_pipeline(deals)}
    elif analysis_type == "revenue":
        return {"revenue_by_sector": analysis_service.analyze_revenue_by_sector(deals)}
    elif analysis_type == "conversion":
        return {"conversion": analysis_service.analyze_conversion_rate(deals, work_orders)}
    elif analysis_type == "delayed":
        return {"delayed_orders": analysis_service.analyze_delayed_orders(work_orders)}
    else:
        return analysis_service.compute_metrics(deals, work_orders)


async def _generate_insight(question: str, metrics: dict, tracker: ToolCallTracker) -> str:
    """Use Gemini to generate a natural language insight from analysis results."""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Send only summaries to Gemini (not the full raw data)
        analysis_text = _extract_summaries(metrics)
        logger.info(f"Sending {len(analysis_text)} chars to Gemini for insight generation")

        response = await asyncio.wait_for(
            asyncio.to_thread(
                model.generate_content,
                INSIGHT_PROMPT.format(question=question, analysis=analysis_text),
            ),
            timeout=GEMINI_TIMEOUT,
        )

        answer = response.text.strip()
        tracker.record("Generate Insight", "Insight generated successfully", "success")
        return answer

    except asyncio.TimeoutError:
        logger.error("Insight generation timed out")
        tracker.record("Generate Insight", "Timed out", "error")
        # Fallback to raw summaries
        return _fallback_summary(metrics)
    except Exception as e:
        logger.error(f"Insight generation failed: {e}")
        tracker.record("Generate Insight", f"Failed: {str(e)}", "error")
        return _fallback_summary(metrics)


def _fallback_summary(metrics: dict) -> str:
    """Return a human-readable summary when Gemini is unavailable."""
    summaries = []
    for key, value in metrics.items():
        if isinstance(value, dict) and "summary" in value:
            summaries.append(value["summary"])
    return " ".join(summaries) if summaries else "Unable to generate insight. Please check API configuration."
