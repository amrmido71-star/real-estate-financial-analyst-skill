# mypy: disable-error-code="no-any-return"
"""revenue_engine.py — Revenue calculations from units and price"""
from typing import List, Dict
from ..base_models import Unit

class RevenueEngine:
    """Calculates GDV, net sales, revenue recognition proxy"""

    @staticmethod
    def calculate_gdv(units: List[Unit]) -> float:  # type: ignore
        return sum(u.price_per_unit for u in units)  # type: ignore

    @staticmethod
    def calculate_gdv_from_mix(unit_mix: List[Dict]) -> float:
        total = 0
        for m in unit_mix:
            cnt = m.get("count", m.get("units", 0))
            price = m.get("price_per_unit", m.get("price", 0))
            if price == 0 and m.get("price_per_sqm") and m.get("area_sqm"):
                price = m["price_per_sqm"] * m["area_sqm"]
            total += cnt * price
        return total

    @staticmethod
    def net_contract_value(list_price: float, discount_pct: float) -> float:
        return list_price * (1 - discount_pct/100)

    @staticmethod
    def price_escalation(base_price_per_sqm: float, annual_growth_pct: float, years: float) -> float:
        return base_price_per_sqm * (1 + annual_growth_pct/100) ** years

    @staticmethod
    def recognized_revenue(contracted_sales: float, progress_pct: float, method: str = "cash_proxy") -> float:
        """Simple: cash_proxy = contracted, poc = contracted * progress"""
        if method == "poc":
            return contracted_sales * progress_pct/100
        return contracted_sales
