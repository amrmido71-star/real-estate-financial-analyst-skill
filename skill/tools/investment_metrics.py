"""
investment_metrics.py — Investment & Valuation Metrics
NPV, IRR, Equity Multiple, Cash-on-Cash, Payback, ROIC
Pure Python — no external dependencies beyond stdlib.
"""

from typing import Optional, List


def calculate_npv(cash_flows: List[float], discount_rate: float, initial_investment: Optional[float] = None) -> Optional[float]:
    """
    NPV = Σ CF_t / (1+r)^t  (t starting at 1)
    If initial_investment provided separately (positive number), it is subtracted as outflow at t=0.
    If cash_flows already includes initial negative at index 0, set initial_investment=None.
    discount_rate as decimal (0.15 = 15%)
    """
    if not cash_flows:
        return None
    if discount_rate is None:
        return None
    npv = 0.0
    for t, cf in enumerate(cash_flows):
        # t=0 is present, not discounted
        if t == 0:
            npv += cf / ((1 + discount_rate) ** 0)
        else:
            npv += cf / ((1 + discount_rate) ** t)
    if initial_investment is not None:
        npv -= initial_investment
    return npv


def calculate_npv_simple(cash_flows: List[float], discount_rate: float) -> Optional[float]:
    """Alias where cash_flows includes initial investment as first element (negative)."""
    return calculate_npv(cash_flows, discount_rate)


def calculate_irr(
    cash_flows: List[float],
    guess: float = 0.1,
    max_iterations: int = 1000,
    tolerance: float = 1e-6,
) -> Optional[float]:
    """
    IRR via Newton-Raphson + fallback to bisection.
    Returns IRR as decimal (0.18 = 18%) or None if not converge / no sign change.
    Requires at least one positive and one negative cash flow.
    """
    if not cash_flows or len(cash_flows) < 2:
        return None

    # Check sign change
    has_positive = any(cf > 0 for cf in cash_flows)
    has_negative = any(cf < 0 for cf in cash_flows)
    if not (has_positive and has_negative):
        return None

    def npv_at(rate: float) -> float:
        total = 0.0
        for t, cf in enumerate(cash_flows):
            total += cf / ((1 + rate) ** t)
        return total

    def npv_derivative(rate: float) -> float:
        total = 0.0
        for t, cf in enumerate(cash_flows):
            if t == 0:
                continue
            total += -t * cf / ((1 + rate) ** (t + 1))
        return total

    # Newton-Raphson
    rate = guess
    for _ in range(max_iterations):
        npv_val = npv_at(rate)
        if abs(npv_val) < tolerance:
            # Validate rate is reasonable: -99% to +1000%
            if -0.99 < rate < 10:
                return rate
            else:
                break
        deriv = npv_derivative(rate)
        if deriv == 0:
            break
        new_rate = rate - npv_val / deriv
        # Prevent divergence: clamp
        if new_rate < -0.99:
            new_rate = -0.99 + 1e-6
        if abs(new_rate - rate) < tolerance:
            if abs(npv_at(new_rate)) < tolerance * 10:
                return new_rate
        rate = new_rate

    # Fallback: Bisection between -0.9 and 5.0 (i.e., -90% to 500%)
    low, high = -0.90, 5.0
    npv_low = npv_at(low)
    npv_high = npv_at(high)

    # Need opposite signs for bisection
    if npv_low * npv_high > 0:
        # Try narrower range
        low, high = -0.5, 2.0
        npv_low = npv_at(low)
        npv_high = npv_at(high)
        if npv_low * npv_high > 0:
            return None

    for _ in range(max_iterations):
        mid = (low + high) / 2
        npv_mid = npv_at(mid)
        if abs(npv_mid) < tolerance:
            return mid
        if npv_low * npv_mid < 0:
            high = mid
            npv_high = npv_mid
        else:
            low = mid
            npv_low = npv_mid
        if (high - low) < tolerance:
            return mid

    return None


def calculate_irr_annualized(monthly_cash_flows: List[float], guess: float = 0.1) -> Optional[float]:
    """
    Calculate IRR from monthly cash flows and annualize: (1 + monthly_irr)^12 - 1
    """
    monthly_irr = calculate_irr(monthly_cash_flows, guess=guess)
    if monthly_irr is None:
        return None
    return (1 + monthly_irr) ** 12 - 1


def calculate_equity_multiple(total_distributions: Optional[float], equity_invested: Optional[float]) -> Optional[float]:
    """Equity Multiple = Total Distributions / Equity Invested"""
    if total_distributions is None or equity_invested is None or equity_invested == 0:
        return None
    return total_distributions / equity_invested


def calculate_cash_on_cash(annual_cash_flow: Optional[float], equity_invested: Optional[float]) -> Optional[float]:
    """Cash-on-Cash % = Annual Cash Flow / Equity Invested * 100"""
    if annual_cash_flow is None or equity_invested is None or equity_invested == 0:
        return None
    return (annual_cash_flow / equity_invested) * 100


def calculate_payback_period(cash_flows: List[float]) -> Optional[float]:
    """
    Payback Period = time to recover initial investment (in same period units as cash_flows)
    Returns fractional period (e.g., 2.5 means 2.5 years if cash_flows are yearly)
    Uses linear interpolation within the payback period.
    If never pays back, returns None.
    """
    if not cash_flows:
        return None
    # Assume first element is initial investment (negative)
    cumulative = 0.0
    for t, cf in enumerate(cash_flows):
        prev_cumulative = cumulative
        cumulative += cf
        if cumulative >= 0 and t > 0:
            # Payback within this period
            if cf == 0:
                return float(t)
            # Fraction = (0 - prev_cumulative) / cf
            fraction = (0 - prev_cumulative) / cf
            return (t - 1) + fraction
        elif t == 0 and cumulative >= 0:
            return 0.0
    return None  # Never pays back


def calculate_roic(nopat: Optional[float], invested_capital: Optional[float]) -> Optional[float]:
    """ROIC % = NOPAT / Invested Capital * 100"""
    if nopat is None or invested_capital is None or invested_capital == 0:
        return None
    return (nopat / invested_capital) * 100


def calculate_nopat(ebit: Optional[float], tax_rate: float) -> Optional[float]:
    """NOPAT = EBIT * (1 - Tax Rate)"""
    if ebit is None:
        return None
    return ebit * (1 - tax_rate)


def calculate_roi_simple(gain: Optional[float], cost: Optional[float]) -> Optional[float]:
    """ROI % = (Gain - Cost)/Cost *100 — same as financial_calculations but alias"""
    if gain is None or cost is None or cost == 0:
        return None
    return ((gain - cost) / cost) * 100
