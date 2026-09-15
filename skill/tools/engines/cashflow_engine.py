"""cashflow_engine.py — Monthly cash flow waterfall"""
from typing import List
from ..cashflow_analysis import build_detailed_cashflow, analyze_cashflow, aggregate_to_quarterly, aggregate_to_annual
from ..base_models import CashFlowPeriod

class CashflowEngine:
    @staticmethod
    def build(periods: List[CashFlowPeriod], opening_cash: float = 0, period_type: str = "monthly"):
        return build_detailed_cashflow(periods, opening_cash, period_type)

    @staticmethod
    def analyze(inflows: List[float], outflows: List[float], financing: List[float] = None, opening: float = 0):
        return analyze_cashflow(inflows, outflows, financing, opening)

    @staticmethod
    def to_quarterly(monthly: List[float]): return aggregate_to_quarterly(monthly)
    @staticmethod
    def to_annual(monthly: List[float]): return aggregate_to_annual(monthly)

    @staticmethod
    def waterfall(collections: float, dev_costs: float, interest: float, debt_repay: float, tax: float = 0):
        """Simple waterfall order"""
        after_dev = collections - dev_costs
        after_interest = after_dev - interest
        after_debt = after_interest - debt_repay
        after_tax = after_debt - tax
        return {
            "after_dev": after_dev,
            "after_interest": after_interest,
            "after_debt": after_debt,
            "after_tax": after_tax,  # distributions
        }
