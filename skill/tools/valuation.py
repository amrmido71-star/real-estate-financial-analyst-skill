"""
valuation.py — Valuation Engine: DCF, Residual Land Value, Comparable, NOI/Cap Rate, WACC
"""

from typing import Optional, List, Dict
from .investment_metrics import calculate_npv


def calculate_wacc(
    cost_of_equity: float,  # e.g., 0.15
    cost_of_debt: float,    # e.g., 0.08
    equity_weight: float,   # e.g., 0.6 (60%)
    debt_weight: float,     # e.g., 0.4
    tax_rate: float = 0.225,
) -> float:
    """
    WACC = Ke * We + Kd * (1 - Tax) * Wd
    """
    if abs(equity_weight + debt_weight - 1.0) > 0.01:
        # Normalize
        total = equity_weight + debt_weight
        equity_weight = equity_weight / total
        debt_weight = debt_weight / total
    return cost_of_equity * equity_weight + cost_of_debt * (1 - tax_rate) * debt_weight


def calculate_cost_of_equity_capm(
    risk_free_rate: float,  # e.g., 0.04
    beta: float,            # e.g., 1.2
    market_risk_premium: float,  # e.g., 0.06
) -> float:
    """CAPM: Ke = Rf + Beta * (MRP)"""
    return risk_free_rate + beta * market_risk_premium


def dcf_valuation(
    cash_flows: List[float],  # [CF0, CF1, CF2, ...], CF0 is period 0 (often 0 or negative)
    discount_rate: float,  # WACC or hurdle
    terminal_value: Optional[float] = None,
    terminal_year: Optional[int] = None,
) -> Dict:
    """
    DCF valuation: NPV of cash flows + discounted terminal value
    """
    npv = calculate_npv(cash_flows, discount_rate)
    pv_terminal = None
    enterprise_value = npv
    if terminal_value is not None:
        t = terminal_year if terminal_year is not None else len(cash_flows) - 1
        # If terminal_year is last index, discount appropriately; if beyond, add extra periods
        # Simple: discount terminal at t
        pv_terminal = terminal_value / ((1 + discount_rate) ** t)
        if npv is not None:
            enterprise_value = npv + pv_terminal
    return {
        "npv_cash_flows": npv,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "discount_rate": discount_rate,
        "terminal_value": terminal_value,
    }


def calculate_terminal_value_gordon(
    final_year_cash_flow: float,
    discount_rate: float,
    perpetual_growth: float = 0.02,
) -> Optional[float]:
    """Gordon Growth: TV = CF_{n+1} / (r - g) = CF_n * (1+g)/(r-g)"""
    if discount_rate <= perpetual_growth:
        return None
    return final_year_cash_flow * (1 + perpetual_growth) / (discount_rate - perpetual_growth)


def calculate_terminal_value_exit_cap(
    noi: float,
    exit_cap_rate: float,  # e.g., 0.08
) -> Optional[float]:
    """Exit Cap: TV = NOI / Cap Rate"""
    if exit_cap_rate == 0:
        return None
    return noi / exit_cap_rate


def residual_land_value(
    gdv: float,
    construction: float = 0,
    soft: float = 0,
    marketing: float = 0,
    financing: float = 0,
    contingency: float = 0,
    fees: float = 0,
    developer_profit: float = 0,  # absolute
    developer_profit_pct_gdv: Optional[float] = None,  # alternative: 20% of GDV
) -> Dict:
    """
    Residual Land Value = GDV - (All costs + Developer Profit)
    """
    if developer_profit_pct_gdv is not None:
        developer_profit = gdv * developer_profit_pct_gdv / 100
    total_costs = construction + soft + marketing + financing + contingency + fees
    land_value = gdv - total_costs - developer_profit
    return {
        "gdv": gdv,
        "total_costs_ex_land": total_costs,
        "developer_profit": developer_profit,
        "residual_land_value": land_value,
        "land_as_pct_gdv": (land_value / gdv * 100) if gdv else None,
    }


def comparable_valuation(
    subject_area_sqm: float,
    comps: List[Dict],  # [{"price_per_sqm":22000, "adjustment_pct":5}, ...]
    subject_adjustment_pct: float = 0,  # overall adjustment
) -> Dict:
    """
    Comparable valuation: average adjusted price/sqm * area
    comps: list with price_per_sqm and optional adjustment_pct
    """
    if not comps or subject_area_sqm == 0:
        return {"value": None, "avg_price_per_sqm": None}
    adjusted_prices = []
    for c in comps:
        p = c.get("price_per_sqm", 0)
        adj = c.get("adjustment_pct", 0)
        adjusted_prices.append(p * (1 + adj / 100))
    avg_price = sum(adjusted_prices) / len(adjusted_prices) if adjusted_prices else 0
    # Apply subject adjustment
    final_price_per_sqm = avg_price * (1 + subject_adjustment_pct / 100)
    value = final_price_per_sqm * subject_area_sqm
    return {
        "avg_comp_price_per_sqm": avg_price,
        "final_price_per_sqm": final_price_per_sqm,
        "subject_area": subject_area_sqm,
        "value": value,
        "comps_used": len(comps),
        "range": {"min": min(adjusted_prices) if adjusted_prices else None, "max": max(adjusted_prices) if adjusted_prices else None},
    }


def income_valuation(
    annual_rent: float,
    vacancy_rate_pct: float = 5.0,
    operating_expenses: float = 0,
    cap_rate: float = 0.08,  # 8%
) -> Dict:
    """
    Income / NOI Valuation: Value = NOI / Cap Rate
    NOI = Effective Gross Income - OpEx
    EGI = Rent * (1 - vacancy)
    """
    egi = annual_rent * (1 - vacancy_rate_pct / 100)
    noi = egi - operating_expenses
    value = (noi / cap_rate) if cap_rate != 0 else None
    noi_margin = (noi / egi * 100) if egi else None
    return {
        "annual_rent": annual_rent,
        "vacancy_pct": vacancy_rate_pct,
        "egi": egi,
        "operating_expenses": operating_expenses,
        "noi": noi,
        "noi_margin_pct": noi_margin,
        "cap_rate": cap_rate,
        "value": value,
        "gross_yield_pct": (annual_rent / value * 100) if value else None,
    }
