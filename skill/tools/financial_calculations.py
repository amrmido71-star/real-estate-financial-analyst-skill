"""
financial_calculations.py — Core profitability, variance & break-even calculations
All functions are guarded against division-by-zero and missing inputs.
"""

from typing import Optional, Literal, Tuple


def calculate_gross_profit(revenue: Optional[float], cost_of_revenue: Optional[float]) -> Optional[float]:
    """Gross Profit = Revenue - Cost of Revenue"""
    if revenue is None or cost_of_revenue is None:
        return None
    return revenue - cost_of_revenue


def calculate_gross_margin(revenue: Optional[float], cost_of_revenue: Optional[float]) -> Optional[float]:
    """Gross Margin % = (Revenue - COR) / Revenue * 100"""
    if revenue is None or cost_of_revenue is None:
        return None
    if revenue == 0:
        return None  # Cannot calculate — denominator zero
    gross_profit = revenue - cost_of_revenue
    return (gross_profit / revenue) * 100


def calculate_operating_profit(gross_profit: Optional[float], operating_expenses: Optional[float]) -> Optional[float]:
    """Operating Profit = Gross Profit - Operating Expenses (S&M + G&A)"""
    if gross_profit is None or operating_expenses is None:
        return None
    return gross_profit - operating_expenses


def calculate_ebitda(operating_profit: Optional[float], depreciation: Optional[float] = 0, amortization: Optional[float] = 0) -> Optional[float]:
    """EBITDA = Operating Profit + Depreciation + Amortization"""
    if operating_profit is None:
        return None
    dep = depreciation or 0
    amort = amortization or 0
    return operating_profit + dep + amort


def calculate_ebit(ebitda: Optional[float], depreciation: Optional[float] = 0, amortization: Optional[float] = 0) -> Optional[float]:
    """EBIT = EBITDA - D&A"""
    if ebitda is None:
        return None
    dep = depreciation or 0
    amort = amortization or 0
    return ebitda - dep - amort


def calculate_net_profit(ebit: Optional[float], interest: Optional[float] = 0, tax: Optional[float] = 0) -> Optional[float]:
    """Net Profit = EBIT - Interest - Tax"""
    if ebit is None:
        return None
    return ebit - (interest or 0) - (tax or 0)


def calculate_net_margin(net_profit: Optional[float], revenue: Optional[float]) -> Optional[float]:
    """Net Margin % = Net Profit / Revenue * 100"""
    if net_profit is None or revenue is None or revenue == 0:
        return None
    return (net_profit / revenue) * 100


def calculate_ebitda_margin(ebitda: Optional[float], revenue: Optional[float]) -> Optional[float]:
    """EBITDA Margin % = EBITDA / Revenue * 100"""
    if ebitda is None or revenue is None or revenue == 0:
        return None
    return (ebitda / revenue) * 100


def calculate_variance(actual: Optional[float], budget: Optional[float]) -> Optional[float]:
    """Absolute Variance = Actual - Budget"""
    if actual is None or budget is None:
        return None
    return actual - budget


def calculate_variance_pct(actual: Optional[float], budget: Optional[float]) -> Optional[float]:
    """Variance % = (Actual - Budget) / |Budget| * 100 — returns None if budget is 0/None"""
    if actual is None or budget is None:
        return None
    if budget == 0:
        return None  # Avoid division by zero; budget zero means % variance undefined
    return ((actual - budget) / abs(budget)) * 100


def classify_variance(
    actual: Optional[float],
    budget: Optional[float],
    is_revenue: bool = False,
    neutral_threshold_pct: float = 2.0,
) -> Literal["Favorable", "Unfavorable", "Neutral", "N/A"]:
    """
    Classify variance as Favorable/Unfavorable/Neutral.
    - Revenue/Inflows: Actual > Budget => Favorable
    - Costs/Outflows: Actual > Budget => Unfavorable
    - Neutral if |Var%| < neutral_threshold_pct
    """
    if actual is None or budget is None:
        return "N/A"
    pct = calculate_variance_pct(actual, budget)
    if pct is None:
        # Budget zero — use absolute comparison
        if actual == budget:
            return "Neutral"
        if actual > budget:
            return "Favorable" if is_revenue else "Unfavorable"
        else:
            return "Unfavorable" if is_revenue else "Favorable"
    if abs(pct) < neutral_threshold_pct:
        return "Neutral"
    if is_revenue:
        return "Favorable" if actual > budget else "Unfavorable"
    else:
        return "Unfavorable" if actual > budget else "Favorable"


def calculate_roi(gain: Optional[float], cost: Optional[float]) -> Optional[float]:
    """ROI % = (Gain - Cost) / Cost * 100 — simple return"""
    if gain is None or cost is None or cost == 0:
        return None
    return ((gain - cost) / cost) * 100


def calculate_roe(net_profit: Optional[float], equity: Optional[float]) -> Optional[float]:
    """ROE % = Net Profit / Equity * 100"""
    if net_profit is None or equity is None or equity == 0:
        return None
    return (net_profit / equity) * 100


def calculate_break_even_sales(fixed_costs: Optional[float], contribution_margin_ratio: Optional[float]) -> Optional[float]:
    """
    Break-even Sales = Fixed Costs / Contribution Margin Ratio
    contribution_margin_ratio is decimal (e.g., 0.35 for 35%)
    """
    if fixed_costs is None or contribution_margin_ratio is None:
        return None
    if contribution_margin_ratio == 0:
        return None
    return fixed_costs / contribution_margin_ratio


def calculate_break_even_units(fixed_costs: Optional[float], price_per_unit: Optional[float], variable_cost_per_unit: Optional[float]) -> Optional[float]:
    """Break-even Units = Fixed Costs / (Price - Variable Cost)"""
    if fixed_costs is None or price_per_unit is None or variable_cost_per_unit is None:
        return None
    contribution = price_per_unit - variable_cost_per_unit
    if contribution == 0:
        return None
    return fixed_costs / contribution


def vertical_analysis(line_item: Optional[float], base: Optional[float]) -> Optional[float]:
    """Vertical % = Line Item / Base (usually Revenue) * 100"""
    if line_item is None or base is None or base == 0:
        return None
    return (line_item / base) * 100


def horizontal_analysis(current: Optional[float], prior: Optional[float]) -> Optional[Tuple[float, float]]:
    """
    Horizontal analysis: returns (absolute_change, pct_change)
    pct_change = (Current - Prior) / |Prior| * 100
    """
    if current is None or prior is None:
        return None
    abs_change = current - prior
    if prior == 0:
        pct_change = None
    else:
        pct_change = (abs_change / abs(prior)) * 100
    return (abs_change, pct_change)  # type: ignore[return-value]
