"""financing_engine.py — Debt schedule, interest, equity"""
from typing import List, Optional
from ..financing import build_financing_schedule, calculate_ltc, calculate_ltv, levered_vs_unlevered, calculate_facility_headroom

class FinancingEngine:
    @staticmethod
    def ltc(debt: float, total_cost: float): return calculate_ltc(debt, total_cost)
    @staticmethod
    def ltv(debt: float, gdv: float): return calculate_ltv(debt, gdv)

    @staticmethod
    def build_schedule(total_debt: float, drawdown: List[float], interest_annual: float, repayment: Optional[List[float]] = None, capitalize: bool = True):
        return build_financing_schedule(total_debt, drawdown, interest_annual, repayment, capitalize_interest=capitalize)

    @staticmethod
    def debt_draw_for_gap(total_need: float, debt_pct: float, collections: float = 0):
        need = total_need - collections
        if need <= 0:
            return 0
        return need * debt_pct/100

    @staticmethod
    def levered(unlevered: List[float], draws: List[float], service: List[float]):
        return levered_vs_unlevered(unlevered, draws, service)

    @staticmethod
    def headroom(limit: float, drawn: float):
        return calculate_facility_headroom(limit, drawn)
