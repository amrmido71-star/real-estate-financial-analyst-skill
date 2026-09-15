"""
investment_metrics.py — Investment & Valuation Metrics
NPV, IRR, MIRR, Equity Multiple, Payback, ROIC
Convention: cash_flows[0] = Period 0 (not discounted), cash_flows[1] = Period 1 (discounted 1 period), etc.
Pure Python — no external dependencies beyond stdlib.
"""

from typing import Optional, List, Tuple
from .exceptions import InvalidDiscountRateError, InvalidCashFlowError, MultipleIRRError, NoIRRError


def calculate_npv(cash_flows: List[float], discount_rate: float) -> Optional[float]:
    """
    NPV = Σ CF_t / (1+r)^t  for t=0..n
    - cash_flows[0] is Period 0 and is NOT discounted (divided by 1)
    - discount_rate as decimal (0.15 = 15%)
    - Returns None for empty input; raises InvalidDiscountRateError if r <= -1
    Mathematically correct and matches Excel NPV if cash_flows[0] is initial investment.

    Examples:
        [-100, 60, 60] @10% => -100 + 54.545 + 49.586 = 4.132
        [-1000, 300, 400, 500] @10% => NPV ≈ 19.1
    """
    if not cash_flows:
        return None
    if discount_rate is None:
        return None
    if discount_rate <= -1:
        raise InvalidDiscountRateError(f"Discount rate must be > -1, got {discount_rate}")
    if discount_rate == -1:
        return None
    npv = 0.0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** t)
    return npv


def calculate_npv_with_initial(cash_flows: List[float], discount_rate: float, initial_investment: float) -> Optional[float]:
    """
    Convenience when initial investment is separate from operating cash flows.
    NPV = -initial_investment + Σ CF_t/(1+r)^t where CF_t starts at t=1

    Example:
        initial=100, cash_flows=[60,60] @10% => -100 + 54.545 + 49.586 = 4.132
        Equivalent to calculate_npv([-100, 60, 60], 0.10)
    """
    if cash_flows is None:
        return None
    combined = [-abs(initial_investment)] + list(cash_flows)
    return calculate_npv(combined, discount_rate)


# Backward compat alias
def calculate_npv_simple(cash_flows: List[float], discount_rate: float) -> Optional[float]:
    return calculate_npv(cash_flows, discount_rate)


def _npv_at(cash_flows: List[float], rate: float) -> float:
    total = 0.0
    for t, cf in enumerate(cash_flows):
        try:
            denom = (1 + rate) ** t
            # Guard extremes
            if denom == 0 or denom == float('inf') or denom == float('-inf'):
                if cf > 0:
                    total += float('inf') if denom == 0 else 0
                elif cf < 0:
                    total += float('-inf') if denom == 0 else 0
                continue
            contrib = cf / denom
            # Clamp infinities
            if contrib == float('inf') or contrib == float('-inf'):
                # Overflow -> treat as large magnitude
                contrib = 1e308 if cf > 0 else -1e308
            total += contrib
        except (OverflowError, ZeroDivisionError, ValueError):
            # If overflow, contribution is effectively 0 for large denom or huge for small denom
            try:
                if rate < -0.5:
                    # small denom -> huge magnitude
                    total += 1e308 if cf > 0 else -1e308
                else:
                    total += 0
            except:
                total += 0
        if total > 1e308:
            total = 1e308
        if total < -1e308:
            total = -1e308
    return total


def _npv_derivative(cash_flows: List[float], rate: float) -> float:
    total = 0.0
    for t, cf in enumerate(cash_flows):
        if t == 0:
            continue
        try:
            denom = (1 + rate) ** (t + 1)
            if denom == 0 or denom == float('inf') or denom == float('-inf'):
                continue
            contrib = -t * cf / denom
            if contrib == float('inf') or contrib == float('-inf'):
                continue
            total += contrib
        except (OverflowError, ZeroDivisionError, ValueError):
            continue
    return total


def count_sign_changes(cash_flows: List[float]) -> int:
    """Count sign changes ignoring zeros"""
    filtered = [cf for cf in cash_flows if cf != 0]
    if len(filtered) < 2:
        return 0
    changes = 0
    for i in range(1, len(filtered)):
        if filtered[i] * filtered[i-1] < 0:
            changes += 1
    return changes


def detect_multiple_irr(cash_flows: List[float]) -> Tuple[bool, int, str]:
    """
    Detect if cash flows may have multiple IRRs.
    Returns (has_multiple_risk, sign_changes, message)
    - 0 or 1 sign change => unique IRR (if exists)
    - >1 sign change => potential multiple IRRs (Descartes' rule)
    """
    changes = count_sign_changes(cash_flows)
    if changes == 0:
        return (False, changes, "No sign change — no IRR exists (all inflows or all outflows)")
    if changes == 1:
        return (False, changes, "One sign change — unique IRR if exists")
    return (True, changes, f"{changes} sign changes — potential multiple IRRs; use MIRR or NPV profile")


def calculate_irr(
    cash_flows: List[float],
    guess: float = 0.1,
    max_iterations: int = 1000,
    tolerance: float = 1e-6,
) -> Optional[float]:
    """
    IRR via Newton-Raphson + bisection fallback.
    Returns IRR as decimal (0.18 = 18%) or None if no IRR exists.
    Convention: cash_flows[0]=Period 0 (undiscounted).

    Detects non-conventional flows but still attempts to find a root.
    Use detect_multiple_irr() to warn caller.
    """
    if not cash_flows or len(cash_flows) < 2:
        return None
    has_positive = any(cf > 0 for cf in cash_flows)
    has_negative = any(cf < 0 for cf in cash_flows)
    if not (has_positive and has_negative):
        return None

    # Newton-Raphson
    rate = guess
    for _ in range(max_iterations):
        npv_val = _npv_at(cash_flows, rate)
        if abs(npv_val) < tolerance:
            if -0.99 < rate < 10:
                return rate
            else:
                break
        deriv = _npv_derivative(cash_flows, rate)
        if deriv == 0:
            break
        new_rate = rate - npv_val / deriv
        if new_rate < -0.99:
            new_rate = -0.99 + 1e-6
        if abs(new_rate - rate) < tolerance:
            if abs(_npv_at(cash_flows, new_rate)) < tolerance * 10:
                return new_rate
        rate = new_rate

    # Bisection fallback
    low, high = -0.90, 5.0
    npv_low = _npv_at(cash_flows, low)
    npv_high = _npv_at(cash_flows, high)
    if npv_low * npv_high > 0:
        low, high = -0.5, 2.0
        npv_low = _npv_at(cash_flows, low)
        npv_high = _npv_at(cash_flows, high)
        if npv_low * npv_high > 0:
            return None
    for _ in range(max_iterations):
        mid = (low + high) / 2
        npv_mid = _npv_at(cash_flows, mid)
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


def calculate_mirr(cash_flows: List[float], finance_rate: float, reinvest_rate: float) -> Optional[float]:
    """
    MIRR = Modified IRR that solves multiple-IRR problem.
    - Negative cash flows discounted to Present at finance_rate
    - Positive cash flows compounded to Future at reinvest_rate
    - MIRR = (FV_positive / -PV_negative)^(1/n) - 1

    finance_rate, reinvest_rate as decimals (0.10 = 10%)
    """
    if not cash_flows or len(cash_flows) < 2:
        return None
    if finance_rate <= -1 or reinvest_rate <= -1:
        raise InvalidDiscountRateError("Rates must be > -1")
    n = len(cash_flows) - 1
    pv_neg = 0.0
    fv_pos = 0.0
    has_neg = False
    has_pos = False
    for t, cf in enumerate(cash_flows):
        if cf < 0:
            has_neg = True
            pv_neg += cf / ((1 + finance_rate) ** t)
        elif cf > 0:
            has_pos = True
            fv_pos += cf * ((1 + reinvest_rate) ** (n - t))
    if not has_neg or not has_pos:
        return None
    if pv_neg == 0:
        return None
    # pv_neg is negative, so -pv_neg is positive
    mirr = (fv_pos / -pv_neg) ** (1 / n) - 1
    return mirr


def calculate_irr_annualized(monthly_cash_flows: List[float], guess: float = 0.1) -> Optional[float]:
    """Annualized IRR from monthly: (1+monthlyIRR)^12 -1"""
    monthly_irr = calculate_irr(monthly_cash_flows, guess=guess)
    if monthly_irr is None:
        return None
    return (1 + monthly_irr) ** 12 - 1


def calculate_equity_multiple(total_distributions: Optional[float], equity_invested: Optional[float]) -> Optional[float]:
    if total_distributions is None or equity_invested is None or equity_invested == 0:
        return None
    return total_distributions / equity_invested


def calculate_cash_on_cash(annual_cash_flow: Optional[float], equity_invested: Optional[float]) -> Optional[float]:
    if annual_cash_flow is None or equity_invested is None or equity_invested == 0:
        return None
    return (annual_cash_flow / equity_invested) * 100


def calculate_payback_period(cash_flows: List[float]) -> Optional[float]:
    """Payback period with linear interpolation; None if never pays back"""
    if not cash_flows:
        return None
    cumulative = 0.0
    for t, cf in enumerate(cash_flows):
        prev = cumulative
        cumulative += cf
        if cumulative >= 0 and t > 0:
            if cf == 0:
                return float(t)
            fraction = (0 - prev) / cf
            return (t - 1) + fraction
        elif t == 0 and cumulative >= 0:
            return 0.0
    return None


def calculate_roic(nopat: Optional[float], invested_capital: Optional[float]) -> Optional[float]:
    if nopat is None or invested_capital is None or invested_capital == 0:
        return None
    return (nopat / invested_capital) * 100


def calculate_nopat(ebit: Optional[float], tax_rate: float) -> Optional[float]:
    if ebit is None:
        return None
    return ebit * (1 - tax_rate)


def calculate_roi_simple(gain: Optional[float], cost: Optional[float]) -> Optional[float]:
    if gain is None or cost is None or cost == 0:
        return None
    return ((gain - cost) / cost) * 100


def irr_with_diagnostics(cash_flows: List[float]) -> dict:
    """Returns dict with irr, sign_changes, has_multiple_risk, mirr, npv_profile hint"""
    changes = count_sign_changes(cash_flows)
    has_multiple, _, msg = detect_multiple_irr(cash_flows)
    irr = calculate_irr(cash_flows)
    # Suggest MIRR if multiple
    mirr = None
    if has_multiple and irr is not None:
        try:
            mirr = calculate_mirr(cash_flows, finance_rate=0.10, reinvest_rate=0.12)
        except Exception:
            mirr = None
    return {
        "irr": irr,
        "irr_pct": irr * 100 if irr is not None else None,
        "sign_changes": changes,
        "has_multiple_risk": has_multiple,
        "message": msg,
        "mirr": mirr,
        "mirr_pct": mirr * 100 if mirr is not None else None,
    }
