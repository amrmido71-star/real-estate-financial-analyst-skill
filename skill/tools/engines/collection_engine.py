"""collection_engine.py — Installment & cash collection schedule"""
from typing import List, Dict
from datetime import date
from collections import defaultdict
from ..sales_collection import build_collection_schedule, spread_monthly_collections

class CollectionEngine:
    @staticmethod
    def build_schedule(contracted_value: float, sale_date: date, collection_assumptions, handover_date: date) -> List[Dict]:
        sched = collection_assumptions.schedule()
        events = build_collection_schedule(contracted_value, sale_date, sched, handover_date)
        # Apply collection rate and lag via spread
        events = spread_monthly_collections(events, collection_assumptions.collection_rate_pct, collection_assumptions.collection_lag_months)
        return events

    @staticmethod
    def aggregate_monthly(sales: List[Dict], collection_assumptions, handover_map: Dict) -> Dict[str, float]:
        monthly = defaultdict(float)
        for s in sales:
            cv = s["contracted_value"]
            sd = s["sale_date"]
            hd = handover_map.get(s.get("unit_code"))
            # Build schedule for this sale
            sched = collection_assumptions.schedule()
            events = build_collection_schedule(cv, sd, sched, hd)
            events = spread_monthly_collections(events, collection_assumptions.collection_rate_pct, collection_assumptions.collection_lag_months)
            for ev in events:
                key = ev["due_date"].strftime("%Y-%m")
                monthly[key] += ev["due_amount"]
        return dict(sorted(monthly.items()))

    @staticmethod
    def aging_analysis(receivables: List[Dict], as_of: date):
        from ..sales_collection import build_aging_buckets, calculate_aging_summary
        buckets = build_aging_buckets(receivables, as_of)
        return calculate_aging_summary(buckets)
