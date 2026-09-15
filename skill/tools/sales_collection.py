"""
sales_collection.py — Sales & Collection Engine
Handles unit inventory, booking/contract/cancellation, installment schedules, collections, aging, velocity
"""

from typing import List, Dict, Optional
from datetime import date, timedelta
from collections import defaultdict


def build_collection_schedule(
    contracted_value: float,
    sale_date: date,
    schedule: List[Dict],  # [{"label":"Booking","pct":10,"months_after_sale":0}, ...]
    handover_date: Optional[date] = None,
) -> List[Dict]:
    """
    Convert installment schedule (pct) into dated collection events.
    schedule example:
        [
          {"label":"Booking", "pct":10, "months_after_sale":0},
          {"label":"Contract", "pct":10, "months_after_sale":1},
          {"label":"During Build", "pct":40, "months_after_sale":6}, # or spread
          {"label":"Handover", "pct":30, "months_after_sale": None, "anchor":"handover"},
          {"label":"Post Handover", "pct":10, "months_after_sale":12},
        ]
    Returns list of {"label","due_date","due_amount"}
    """
    result = []
    for inst in schedule:
        pct = inst.get("pct", 0)
        amount = contracted_value * pct / 100
        anchor = inst.get("anchor")
        if anchor == "handover" and handover_date:
            # If handover, use handover_date + offset months
            offset = inst.get("months_after_handover", 0)
            due = handover_date + timedelta(days=30 * offset)
        else:
            months = inst.get("months_after_sale", 0) or 0
            # Approximate: 30 days per month
            due = sale_date + timedelta(days=30 * months)
        result.append({
            "label": inst.get("label", ""),
            "pct": pct,
            "due_date": due,
            "due_amount": round(amount, 2),
        })
    return result


def spread_monthly_collections(
    collection_events: List[Dict],
    collection_rate: float = 100.0,  # % collected on time
    delay_months: int = 0,
) -> List[Dict]:
    """
    Apply collection efficiency and delay: only collection_rate% collected on due date,
    remainder delayed. Simplified: spread evenly or delay.
    Returns adjusted events with effective dates.
    """
    if collection_rate >= 100 and delay_months == 0:
        return collection_events
    adjusted = []
    for ev in collection_events:
        due_amount = ev["due_amount"]
        on_time = due_amount * collection_rate / 100
        delayed = due_amount - on_time
        # On-time portion
        adjusted.append({**ev, "due_amount": round(on_time, 2), "is_delayed": False})
        if delayed > 0.01:
            delayed_event = {**ev, "due_amount": round(delayed, 2), "is_delayed": True}
            delayed_event["due_date"] = ev["due_date"] + timedelta(days=30 * max(1, delay_months))
            delayed_event["label"] = ev["label"] + " (Delayed)"
            adjusted.append(delayed_event)
    return adjusted


def aggregate_monthly_cash(
    sales: List[Dict],  # [{"contracted_value","sale_date","schedule"}]
    handover_dates: Optional[Dict] = None,
    collection_rate: float = 90.0,
    delay_months: int = 0,
) -> Dict[str, float]:
    """
    Aggregate sales into monthly cash collections dict: {"YYYY-MM": amount}
    """
    monthly = defaultdict(float)  # type: ignore[var-annotated]
    for s in sales:
        cv = s.get("contracted_value", 0)
        sd = s.get("sale_date")
        sched = s.get("schedule", [])
        hd = None
        if handover_dates and s.get("unit_code"):
            hd = handover_dates.get(s["unit_code"])
        events = build_collection_schedule(cv, sd, sched, hd)  # type: ignore[arg-type]
        events = spread_monthly_collections(events, collection_rate, delay_months)
        for ev in events:
            key = ev["due_date"].strftime("%Y-%m")
            monthly[key] += ev["due_amount"]
    return dict(sorted(monthly.items()))


def calculate_sales_metrics(
    units: List[Dict],
) -> Dict:
    """
    units: list of {"unit_code","status","price_per_unit","area"}
    Returns dict with total, sold, available, rate, ASP, price/sqm, cancellation
    """
    total = len(units)
    sold = sum(1 for u in units if u.get("status") == "sold")
    available = sum(1 for u in units if u.get("status") == "available")
    reserved = sum(1 for u in units if u.get("status") == "reserved")
    cancelled = sum(1 for u in units if u.get("status") == "cancelled")
    sold_units = [u for u in units if u.get("status") == "sold"]
    total_sales_value = sum(u.get("price_per_unit", 0) for u in sold_units)
    total_area_sold = sum(u.get("area", 0) for u in sold_units)
    asp = total_sales_value / sold if sold else None
    price_per_sqm = total_sales_value / total_area_sold if total_area_sold else None
    sales_rate = (sold / total * 100) if total else None
    cancellation_rate = (cancelled / (sold + cancelled) * 100) if (sold + cancelled) else 0.0
    return {
        "total_units": total,
        "sold_units": sold,
        "available_units": available,
        "reserved_units": reserved,
        "cancelled_units": cancelled,
        "sales_rate_pct": sales_rate,
        "total_sales_value": total_sales_value,
        "asp": asp,
        "price_per_sqm": price_per_sqm,
        "cancellation_rate_pct": cancellation_rate,
        "total_area_sold": total_area_sold,
    }


def calculate_collection_metrics_detailed(
    contracted: float,
    collected: float,
    due: float,
) -> Dict:
    outstanding = contracted - collected if contracted is not None and collected is not None else None
    efficiency = (collected / due * 100) if due and due != 0 else None
    overdue = (due - collected) if due is not None and collected is not None else None
    if overdue is not None and overdue < 0:
        overdue = 0
    overdue_pct = (overdue / due * 100) if due and overdue is not None else None
    return {
        "contracted": contracted,
        "collected": collected,
        "due": due,
        "outstanding_receivables": outstanding,
        "collection_efficiency_pct": efficiency,
        "overdue_amount": overdue,
        "overdue_pct": overdue_pct,
    }


def build_aging_buckets(
    receivables: List[Dict],  # [{"due_date":date, "due_amount":float, "collected":bool}]
    as_of: date,
) -> Dict[str, float]:
    """
    Buckets: 0-30, 31-60, 61-90, 91-180, 180+
    Only for overdue (due_date < as_of and not collected)
    """
    buckets = {"0-30": 0.0, "31-60": 0.0, "61-90": 0.0, "91-180": 0.0, "180+": 0.0}
    for r in receivables:
        if r.get("collected"):
            continue
        due = r.get("due_date")
        amt = r.get("due_amount", 0)
        if due is None or due >= as_of:
            continue
        days_overdue = (as_of - due).days
        if days_overdue <= 30:
            buckets["0-30"] += amt
        elif days_overdue <= 60:
            buckets["31-60"] += amt
        elif days_overdue <= 90:
            buckets["61-90"] += amt
        elif days_overdue <= 180:
            buckets["91-180"] += amt
        else:
            buckets["180+"] += amt
    return buckets


def calculate_aging_summary(buckets: Dict[str, float]) -> Dict:
    total_overdue = sum(buckets.values())
    overdue_90_plus = buckets.get("91-180", 0) + buckets.get("180+", 0)
    overdue_pct_90 = (overdue_90_plus / total_overdue * 100) if total_overdue else 0
    return {
        "buckets": buckets,
        "total_overdue": total_overdue,
        "overdue_90_plus": overdue_90_plus,
        "overdue_90_plus_pct": overdue_pct_90,
        "risk_flag": overdue_90_plus and overdue_90_plus / total_overdue > 0.20 if total_overdue else False,
    }


def calculate_sales_velocity(
    sales_per_month: List[int],  # e.g., [10,12,8,15]
) -> Dict:
    if not sales_per_month:
        return {"avg_monthly": None, "total": 0, "trend": None}
    avg = sum(sales_per_month) / len(sales_per_month)
    # Trend: last 3 vs first 3
    if len(sales_per_month) >= 6:
        first = sum(sales_per_month[:3]) / 3
        last = sum(sales_per_month[-3:]) / 3
        trend = "up" if last > first * 1.1 else "down" if last < first * 0.9 else "stable"
    else:
        trend = "insufficient_data"
    return {
        "avg_monthly": avg,
        "total": sum(sales_per_month),
        "trend": trend,
        "monthly": sales_per_month,
    }


def calculate_expected_collection(
    contracted: float,
    collection_rate: float,  # 0-100
) -> float:
    return contracted * collection_rate / 100
