"""
Business Intelligence analysis service.
Computes pipeline health, revenue, conversions, and delayed orders.
"""

from datetime import datetime
from collections import defaultdict
from utils.logger import logger


def analyze_pipeline(deals: list[dict]) -> dict:
    """
    Analyze deal pipeline health: total deals, stage distribution, total value.
    """
    if not deals:
        return {"total_deals": 0, "stages": {}, "total_pipeline_value": 0, "summary": "No deals data available."}

    stages = defaultdict(int)
    total_value = 0.0

    for deal in deals:
        # Look for status/stage fields
        stage = deal.get("deal_status", deal.get("status", "unknown"))
        stages[stage] += 1

        # Look for value fields
        for key in ["deal_value", "value", "amount", "order_value", "revenue"]:
            if key in deal and isinstance(deal[key], (int, float)):
                total_value += deal[key]
                break

    stage_dict = dict(stages)
    total_deals = len(deals)

    summary = f"Pipeline has {total_deals} deals worth ₹{total_value:,.0f}. "
    if stage_dict:
        top_stage = max(stage_dict, key=stage_dict.get)
        summary += f"Most deals are in '{top_stage}' stage ({stage_dict[top_stage]} deals)."

    return {
        "total_deals": total_deals,
        "stages": stage_dict,
        "total_pipeline_value": total_value,
        "summary": summary,
    }


def analyze_revenue_by_sector(deals: list[dict]) -> dict:
    """
    Group deals by sector and compute revenue for each.
    """
    if not deals:
        return {"sectors": {}, "summary": "No deals data available."}

    sectors = defaultdict(lambda: {"count": 0, "value": 0.0})

    for deal in deals:
        sector = deal.get("sector", deal.get("category", deal.get("client_code", "unknown")))

        sectors[sector]["count"] += 1

        for key in ["deal_value", "value", "amount", "order_value", "revenue"]:
            if key in deal and isinstance(deal[key], (int, float)):
                sectors[sector]["value"] += deal[key]
                break

    sector_dict = dict(sectors)

    if sector_dict:
        top_sector = max(sector_dict, key=lambda s: sector_dict[s]["value"])
        summary = f"Top sector by revenue: '{top_sector}' with ₹{sector_dict[top_sector]['value']:,.0f} across {sector_dict[top_sector]['count']} deals."
    else:
        summary = "No sector data available."

    return {"sectors": sector_dict, "summary": summary}


def analyze_conversion_rate(deals: list[dict], work_orders: list[dict]) -> dict:
    """
    Compute deal-to-work-order conversion rate.
    """
    total_deals = len(deals)
    total_work_orders = len(work_orders)

    if total_deals == 0:
        return {
            "total_deals": 0,
            "total_work_orders": total_work_orders,
            "conversion_rate": 0,
            "summary": "No deals data to compute conversion rate.",
        }

    conversion_rate = (total_work_orders / total_deals) * 100

    summary = (
        f"Out of {total_deals} deals, {total_work_orders} have converted to work orders "
        f"({conversion_rate:.1f}% conversion rate)."
    )

    return {
        "total_deals": total_deals,
        "total_work_orders": total_work_orders,
        "conversion_rate": round(conversion_rate, 1),
        "summary": summary,
    }


def analyze_delayed_orders(work_orders: list[dict]) -> dict:
    """
    Identify work orders that are past their delivery date.
    """
    if not work_orders:
        return {"total_orders": 0, "delayed_count": 0, "delayed_orders": [], "summary": "No work orders data available."}

    today = datetime.now().strftime("%Y-%m-%d")
    delayed = []

    for wo in work_orders:
        delivery_date = wo.get("delivery_date", wo.get("deadline", wo.get("due_date")))
        status = wo.get("execution_status", wo.get("status", "unknown"))

        if delivery_date and delivery_date < today and status not in ("done", "completed", "delivered"):
            delayed.append({
                "name": wo.get("name", "Unknown"),
                "delivery_date": delivery_date,
                "status": status,
            })

    total_orders = len(work_orders)
    delayed_count = len(delayed)

    summary = f"{delayed_count} out of {total_orders} work orders are delayed."
    if delayed_count > 0:
        summary += f" Earliest delayed: '{delayed[0]['name']}' (due: {delayed[0]['delivery_date']})."

    return {
        "total_orders": total_orders,
        "delayed_count": delayed_count,
        "delayed_orders": delayed[:10],  # Limit to 10 for response size
        "summary": summary,
    }


def compute_metrics(deals: list[dict], work_orders: list[dict]) -> dict:
    """
    Run all BI analyses and return a comprehensive metrics summary.
    """
    logger.info("Computing business intelligence metrics")

    pipeline = analyze_pipeline(deals)
    revenue = analyze_revenue_by_sector(deals)
    conversion = analyze_conversion_rate(deals, work_orders)
    delayed = analyze_delayed_orders(work_orders)

    return {
        "pipeline": pipeline,
        "revenue_by_sector": revenue,
        "conversion": conversion,
        "delayed_orders": delayed,
        "overall_summary": (
            f"{pipeline['summary']} "
            f"{revenue['summary']} "
            f"{conversion['summary']} "
            f"{delayed['summary']}"
        ),
    }
