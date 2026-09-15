"""construction_engine.py — Construction cost S-Curve and EAC"""
from typing import List, Dict, Optional
from ..construction_analysis import generate_s_curve, analyze_construction

class ConstructionEngine:
    @staticmethod
    def build_curve(budget: float, months: int, curve_type: str = "s_curve", custom_curve: Optional[List[float]] = None, escalation_pct: float = 0.0) -> List[float]:
        if escalation_pct != 0:
            budget = budget * (1 + escalation_pct/100) ** (months/12)
        if curve_type == "custom" and custom_curve:
            total_w = sum(custom_curve)
            return [budget * w/total_w for w in custom_curve]
        type_map = {"s_curve":"standard","linear":"linear","front_loaded":"front_loaded","back_loaded":"back_loaded"}
        curve = type_map.get(curve_type, "standard")
        return generate_s_curve(budget, months, curve)

    @staticmethod
    def analyze(budget: float, actual: float, etc: float, pct_complete: Optional[float] = None) -> Dict:
        return analyze_construction(budget, actual, etc, pct_complete)

    @staticmethod
    def eac(actual: float, etc: float) -> float:
        return actual + etc
