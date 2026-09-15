import pytest
from datetime import date
from skill.tools.sales_collection import (
    build_collection_schedule, aggregate_monthly_cash, calculate_sales_metrics,
    calculate_collection_metrics_detailed, build_aging_buckets, calculate_aging_summary,
    calculate_sales_velocity, spread_monthly_collections
)

def test_build_collection_schedule():
    sched = [
        {"label":"Booking","pct":10,"months_after_sale":0},
        {"label":"Contract","pct":10,"months_after_sale":1},
        {"label":"Handover","pct":80,"months_after_sale":12},
    ]
    events = build_collection_schedule(1_000_000, date(2025,1,15), sched)
    assert len(events) == 3
    assert events[0]["due_amount"] == 100000
    assert events[1]["due_amount"] == 100000
    assert events[2]["due_amount"] == 800000
    assert events[0]["due_date"] == date(2025,1,15)

def test_build_schedule_with_handover():
    sched = [
        {"label":"Booking","pct":20,"months_after_sale":0},
        {"label":"Handover","pct":80,"anchor":"handover","months_after_handover":0},
    ]
    handover = date(2026,6,1)
    events = build_collection_schedule(500000, date(2025,1,1), sched, handover)
    assert events[1]["due_date"] == handover

def test_spread_collections_efficiency():
    events = [{"label":"Booking","due_date":date(2025,1,1),"due_amount":100000,"pct":10}]
    adjusted = spread_monthly_collections(events, collection_rate=80, delay_months=2)
    assert len(adjusted) == 2
    assert adjusted[0]["due_amount"] == 80000
    assert adjusted[1]["due_amount"] == 20000
    assert adjusted[1]["is_delayed"]

def test_aggregate_monthly_cash():
    sales = [
        {"contracted_value": 1000000, "sale_date": date(2025,1,15), "schedule": [
            {"label":"Booking","pct":10,"months_after_sale":0},
            {"label":"Balance","pct":90,"months_after_sale":6},
        ]},
        {"contracted_value": 2000000, "sale_date": date(2025,1,20), "schedule": [
            {"label":"Booking","pct":10,"months_after_sale":0},
            {"label":"Balance","pct":90,"months_after_sale":6},
        ]},
    ]
    monthly = aggregate_monthly_cash(sales, collection_rate=100)
    # Jan should have 10% of both =100k+200k=300k
    jan = monthly.get("2025-01", 0)
    assert jan == 300000
    # July should have 90% =900k+1800k=2700k
    july = monthly.get("2025-07", 0)
    assert july == 2700000

def test_calculate_sales_metrics():
    units = [
        {"unit_code":"A1","status":"sold","price_per_unit":2000000,"area":100},
        {"unit_code":"A2","status":"sold","price_per_unit":3000000,"area":150},
        {"unit_code":"A3","status":"available","price_per_unit":2500000,"area":120},
        {"unit_code":"A4","status":"cancelled","price_per_unit":2000000,"area":100},
    ]
    m = calculate_sales_metrics(units)
    assert m["total_units"] == 4
    assert m["sold_units"] == 2
    assert m["available_units"] == 1
    assert m["cancelled_units"] == 1
    assert m["sales_rate_pct"] == 50.0
    assert m["total_sales_value"] == 5000000
    assert m["asp"] == 2500000
    assert m["price_per_sqm"] == 20000  # 5M /250

def test_calculate_collection_metrics():
    res = calculate_collection_metrics_detailed(1000000, 800000, 1000000)
    assert res["outstanding_receivables"] == 200000
    assert res["collection_efficiency_pct"] == 80.0
    assert res["overdue_amount"] == 200000

def test_aging_buckets():
    as_of = date(2025,6,30)
    receivables = [
        {"due_date": date(2025,6,10), "due_amount": 10000, "collected": False}, # 20 days
        {"due_date": date(2025,5,1), "due_amount": 20000, "collected": False},  # 60 days
        {"due_date": date(2025,3,1), "due_amount": 30000, "collected": False},  # 121 days
        {"due_date": date(2024,12,1), "due_amount": 40000, "collected": False}, # 211 days
        {"due_date": date(2025,6,15), "due_amount": 50000, "collected": True},  # collected, ignore
    ]
    buckets = build_aging_buckets(receivables, as_of)
    assert buckets["0-30"] == 10000
    assert buckets["31-60"] == 20000
    assert buckets["91-180"] == 30000
    assert buckets["180+"] == 40000
    summary = calculate_aging_summary(buckets)
    assert summary["total_overdue"] == 100000  # 10+20+30+40
    assert summary["overdue_90_plus"] == 70000
    assert summary["risk_flag"]  # 70% >20%

def test_sales_velocity():
    v = calculate_sales_velocity([10,12,8,15,9,11])
    assert v["avg_monthly"] == pytest.approx(10.833, rel=1e-2)
    assert v["total"] == 65
    assert v["trend"] in ["up","down","stable","insufficient_data"]

def test_sales_velocity_up_trend():
    v = calculate_sales_velocity([5,5,5,10,10,10])
    assert v["trend"] == "up"
