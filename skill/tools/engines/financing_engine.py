"""financing_engine.py — Debt schedule, interest, equity (Single Source of Truth for LTC/Interest)"""
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
    def debt_draw_for_gap(total_cost: float, debt_pct: float, collections: float = 0, total_need: float | None = None) -> float:
        """
        Single source for LTC-based draw.
        Logic: need = total_cost - collections (or total_need if provided)
        target = total_cost * debt_pct/100 (LTC cap)
        draw = min(target, max(0, need)) if need>0 else 0
        Documented: debt is % of cost, capped by funding gap.
        """
        if total_need is not None:
            need = total_need
        else:
            need = total_cost - collections
        if need <= 0:
            return 0.0
        target = total_cost * debt_pct / 100
        return min(target, need)

    @staticmethod
    def monthly_interest(opening_debt: float, annual_rate_pct: float) -> float:
        """Monthly periodic rate = annual nominal / 12. Single source."""
        return opening_debt * (annual_rate_pct / 100 / 12)

    @staticmethod
    def levered(unlevered: List[float], draws: List[float], service: List[float]):
        return levered_vs_unlevered(unlevered, draws, service)

    @staticmethod
    def headroom(limit: float, drawn: float):
        return calculate_facility_headroom(limit, drawn)

    @staticmethod
    def debt_reconciliation_check(opening: float, draw: float, interest_accrued: float, repayment: float, closing: float, capitalized: bool = True, tol: float = 0.01) -> bool:
        """Check: opening + draw + (interest if capitalized else 0) - repayment == closing within tol"""
        expected = opening + draw + (interest_accrued if capitalized else 0) - repayment
        return abs(expected - closing) <= tol
