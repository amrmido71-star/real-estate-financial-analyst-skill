"""sales_engine.py — Unit inventory & sales velocity"""
from typing import List, Dict, Optional
from datetime import date
from ..base_models import Unit

class SalesEngine:
    @staticmethod
    def build_sales_schedule(total_units: int, velocity_per_month: float, months: int, monthly_schedule: Optional[List[int]] = None) -> List[int]:
        if monthly_schedule:
            sched = list(monthly_schedule)
            if len(sched) < months:
                sched += [0]*(months-len(sched))
            return sched[:months]
        # velocity-based
        remaining = total_units
        sched = []
        for m in range(months):
            if remaining <=0:
                sched.append(0)
            else:
                sell = min(int(round(velocity_per_month)), remaining)
                sched.append(sell)
                remaining -= sell
        # Adjust to exactly total_units
        total = sum(sched)
        if total < total_units:
            for i in range(total_units - total):
                sched[i % months] += 1
        elif total > total_units:
            excess = total - total_units
            for i in range(len(sched)-1, -1, -1):
                if excess <= 0:
                    break
                take = min(sched[i], excess)
                sched[i]-=take
                excess-=take
        return sched

    @staticmethod
    def assign_sales_to_units(units: List[Unit], monthly_schedule: List[int], start_date: date) -> Dict[str, date]:
        """Returns unit_code -> sale_date"""
        mapping = {}
        idx = 0
        for m, cnt in enumerate(monthly_schedule):
            sdate = date(start_date.year + (start_date.month-1+m)//12, (start_date.month-1+m)%12+1, 1)
            for _ in range(cnt):
                if idx < len(units):
                    units[idx].status = "sold"
                    mapping[units[idx].unit_code] = sdate
                    idx+=1
        return mapping

    @staticmethod
    def sales_metrics(total_units: int, sold_units: int, cancelled: int = 0) -> Dict:
        return {
            "total_units": total_units,
            "sold_units": sold_units,
            "remaining_units": total_units - sold_units,
            "sales_rate_pct": sold_units/total_units*100 if total_units else 0,
            "cancellation_rate_pct": cancelled/(sold_units+cancelled)*100 if (sold_units+cancelled) else 0,
        }
