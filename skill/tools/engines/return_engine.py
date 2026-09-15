"""return_engine.py — IRR, NPV, MOIC, DSCR, break-even, valuation"""
from typing import List, Optional
from ..investment_metrics import calculate_irr, calculate_npv, calculate_mirr, calculate_payback_period
from ..valuation import calculate_wacc, dcf_valuation
from ..project_metrics import calculate_development_margin, calculate_break_even_revenue

class ReturnEngine:
    @staticmethod
    def irr(cash_flows: List[float]): return calculate_irr(cash_flows)
    @staticmethod
    def npv(cash_flows: List[float], rate: float): return calculate_npv(cash_flows, rate)
    @staticmethod
    def mirr(cash_flows: List[float], finance: float = 0.10, reinvest: float = 0.12): return calculate_mirr(cash_flows, finance, reinvest)
    @staticmethod
    def moic(distributions: float, equity: float): return distributions/equity if equity else None
    @staticmethod
    def payback(cfs: List[float]): return calculate_payback_period(cfs)
    @staticmethod
    def margin(gdv: float, gdc: float): return calculate_development_margin(gdv, gdc)
    @staticmethod
    def profit_on_cost(gdv: float, gdc: float): return (gdv-gdc)/gdc*100 if gdc else None
    @staticmethod
    def wacc(ke: float, kd: float, we: float, wd: float, tax: float): return calculate_wacc(ke, kd, we, wd, tax)
    @staticmethod
    def break_even_revenue(gdc: float, target_margin: float): return calculate_break_even_revenue(gdc, target_margin)
    @staticmethod
    def dcf(cfs: List[float], rate: float, tv: Optional[float] = None): return dcf_valuation(cfs, rate, tv)
