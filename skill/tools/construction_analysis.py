"""
construction_analysis.py — Construction Cost & Progress Engine
Supports Budget vs Actual vs ETC vs EAC, Variance, S-Curve
"""

from typing import List, Dict, Optional, Tuple


def calculate_eac(actual: float, etc: float) -> float:
    """Estimate at Completion = Actual + Estimate to Complete"""
    return actual + etc


def calculate_etc(budget: float, actual: float, pct_complete: Optional[float] = None, re_estimate: Optional[float] = None) -> float:
    """
    ETC calculation:
    - If re_estimate provided, use it
    - Else if pct_complete provided: ETC = (Budget - Actual) / pct_complete? Simplified: Budget - Actual
    - Else: Budget - Actual (remaining budget)
    """
    if re_estimate is not None:
        return re_estimate
    # Simplified: remaining budget
    return max(0, budget - actual)


def calculate_variance(budget: float, actual_or_eac: float) -> Tuple[float, Optional[float]]:
    """
    Returns (variance_abs, variance_pct)
    variance_abs = Budget - Actual (positive = under budget)
    For cost, negative variance = over budget (unfavorable)
    variance_pct = variance_abs / Budget *100
    """
    var_abs = budget - actual_or_eac
    var_pct = (var_abs / budget * 100) if budget != 0 else None
    return (var_abs, var_pct)


def classify_cost_variance(budget: float, actual: float, neutral_pct: float = 2.0) -> str:
    var_abs, var_pct = calculate_variance(budget, actual)
    if var_pct is None:
        return "N/A"
    if abs(var_pct) < neutral_pct:
        return "Neutral"
    # For cost: actual > budget => overrun => Unfavorable
    return "Unfavorable" if actual > budget else "Favorable"


def generate_s_curve(
    total_cost: float,
    months: int,
    curve_type: str = "standard",  # standard, front_loaded, back_loaded, linear
) -> List[float]:
    """
    Generate S-Curve monthly cost distribution.
    Standard: slow start, peak middle, taper end (approx. using sine-based)
    Returns list of monthly costs summing to total_cost
    """
    if months <= 0:
        return []
    if curve_type == "linear":
        monthly = [total_cost / months] * months
        return monthly
    # S-curve via cumulative using cubic: cum = 3*(t/T)^2 -2*(t/T)^3 (smooth S)
    # For front/back loaded, adjust exponent
    weights = []
    for m in range(1, months + 1):
        t = m / months
        t_prev = (m - 1) / months
        if curve_type == "standard":
            cum = 3 * t**2 - 2 * t**3
            cum_prev = 3 * t_prev**2 - 2 * t_prev**3
        elif curve_type == "front_loaded":
            # Earlier peak: use t^0.8
            cum = t ** 0.7
            cum_prev = t_prev ** 0.7
            # Normalize to S shape still but front loaded
            # Approximate: weight proportional to (1 - t + 0.3)
            # Simpler: use linear interpolation for front
            pass
        elif curve_type == "back_loaded":
            cum = t ** 2.5
            cum_prev = t_prev ** 2.5
        else:
            cum = t
            cum_prev = t_prev
        # For front_loaded we did not compute correctly above, so handle separately
        if curve_type == "front_loaded":
            # front: 40% in first 30%, 35% next 40%, 25% last 30%
            if t <= 0.3:
                # First 30% of time → 40% of cost
                cum = (t / 0.3) * 0.4
                cum_prev = (t_prev / 0.3) * 0.4 if t_prev <= 0.3 else 0.4
            elif t <= 0.7:
                cum = 0.4 + ((t - 0.3) / 0.4) * 0.35
                cum_prev = 0.4 + ((t_prev - 0.3) / 0.4) * 0.35 if t_prev > 0.3 else 0.4
            else:
                cum = 0.75 + ((t - 0.7) / 0.3) * 0.25
                cum_prev = 0.75 + ((t_prev - 0.7) / 0.3) * 0.25 if t_prev > 0.7 else 0.75
        weight = cum - cum_prev
        weights.append(max(0, weight))
    # Normalize weights to sum 1
    total_w = sum(weights)
    if total_w == 0:
        return [total_cost / months] * months
    monthly = [total_cost * w / total_w for w in weights]
    # Adjust rounding to match total exactly
    diff = total_cost - sum(monthly)
    monthly[-1] += diff
    return monthly


def analyze_construction(
    budget: float,
    actual: float,
    etc: Optional[float] = None,
    pct_complete: Optional[float] = None,  # 0-100
    commitments: Optional[float] = None,
) -> Dict:
    """
    Full construction analysis
    """
    if etc is None:
        etc = calculate_etc(budget, actual, pct_complete)
    eac = calculate_eac(actual, etc)
    var_budget_actual_abs, var_budget_actual_pct = calculate_variance(budget, actual)
    var_budget_eac_abs, var_budget_eac_pct = calculate_variance(budget, eac)
    # Cost to complete vs remaining budget
    remaining_budget = budget - actual
    # Progress analysis
    if pct_complete is not None and pct_complete > 0:
        # Earned Value style: CPI = Earned / Actual, SPI = Earned / Planned
        earned = budget * pct_complete / 100
        cpi = earned / actual if actual != 0 else None
        # Estimate: if CPI <1, overrun trending
    else:
        earned = None
        cpi = None

    classification_actual = classify_cost_variance(budget, actual)
    classification_eac = classify_cost_variance(budget, eac)

    return {
        "budget": budget,
        "actual": actual,
        "etc": etc,
        "eac": eac,
        "commitments": commitments,
        "variance_budget_vs_actual_abs": var_budget_actual_abs,
        "variance_budget_vs_actual_pct": var_budget_actual_pct,
        "variance_budget_vs_eac_abs": var_budget_eac_abs,
        "variance_budget_vs_eac_pct": var_budget_eac_pct,
        "remaining_budget": remaining_budget,
        "cost_to_complete": etc,
        "pct_complete": pct_complete,
        "earned_value": earned,
        "cpi": cpi,
        "classification_actual": classification_actual,
        "classification_eac": classification_eac,
        "overrun_risk": eac > budget * 1.05 if budget else False,
    }


def monthly_progress_report(
    monthly_budget: List[float],
    monthly_actual: List[float],
    labels: Optional[List[str]] = None,
) -> List[Dict]:
    """
    Compare monthly budget vs actual with cumulative
    """
    n = max(len(monthly_budget), len(monthly_actual))
    budget = (monthly_budget + [0]*(n - len(monthly_budget)))[:n]
    actual = (monthly_actual + [0]*(n - len(monthly_actual)))[:n]
    result = []
    cum_b = 0
    cum_a = 0
    for i in range(n):
        cum_b += budget[i]  # type: ignore[assignment]
        cum_a += actual[i]  # type: ignore[assignment]
        var = budget[i] - actual[i]
        var_pct = (var / budget[i] * 100) if budget[i] != 0 else None
        cum_var = cum_b - cum_a
        cum_var_pct = (cum_var / cum_b * 100) if cum_b != 0 else None
        result.append({
            "period": labels[i] if labels and i < len(labels) else f"M{i+1}",
            "budget": budget[i],
            "actual": actual[i],
            "variance_abs": var,
            "variance_pct": var_pct,
            "cumulative_budget": cum_b,
            "cumulative_actual": cum_a,
            "cumulative_variance_abs": cum_var,
            "cumulative_variance_pct": cum_var_pct,
        })
    return result
