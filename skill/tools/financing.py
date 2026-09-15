"""
financing.py — Financing Engine for Real Estate Development
Supports Equity/Debt, LTC, LTV, Drawdown, Repayment, Interest, DSCR, Headroom
"""

from typing import List, Dict, Optional


def calculate_ltc(debt: float, total_cost: float) -> Optional[float]:
    """Loan to Cost % = Debt / Total Cost *100"""
    if total_cost == 0 or total_cost is None:
        return None
    return debt / total_cost * 100


def calculate_ltv(debt: float, gdv: float) -> Optional[float]:
    if gdv == 0 or gdv is None:
        return None
    return debt / gdv * 100


def calculate_debt_to_equity(debt: float, equity: float) -> Optional[float]:
    if equity == 0 or equity is None:
        return None
    return debt / equity


def build_financing_schedule(
    total_debt: float,
    drawdown_schedule: List[float],  # per period amounts or % (if sum != total, treat as %)
    interest_rate_annual: float,  # e.g., 0.12
    repayment_schedule: Optional[List[float]] = None,  # per period principal repayment
    periods_per_year: int = 12,
    capitalize_interest: bool = True,
) -> List[Dict]:
    """
    Build period-by-period financing schedule.
    Returns list of {"period","drawdown","interest","repayment","balance","capitalized"}
    """
    # Normalize drawdown: if sum approx total, use as amounts; else treat as %?
    # Simplistic: if any drawdown > total_debt, treat as % (0-100)
    # Otherwise treat as amounts that should sum to total_debt
    is_pct = False
    if drawdown_schedule and max(drawdown_schedule) <= 1.5 and sum(drawdown_schedule) <= 1.5:
        # Looks like decimals (0.2 =20%)
        is_pct = True
    drawdowns = []
    if is_pct:
        drawdowns = [total_debt * p for p in drawdown_schedule]
    else:
        drawdowns = drawdown_schedule[:]
        # If sum != total but not pct, just use as given (allow under-draw)

    n = max(len(drawdowns), len(repayment_schedule) if repayment_schedule else 0)
    if n == 0:
        n = 1
    drawdowns = (drawdowns + [0]*(n - len(drawdowns)))[:n]
    repayments = (repayment_schedule + [0]*(n - len(repayment_schedule)))[:n] if repayment_schedule else [0]*n

    monthly_rate = interest_rate_annual / periods_per_year
    balance = 0.0
    schedule = []
    for i in range(n):
        draw = drawdowns[i]
        balance += draw
        interest = balance * monthly_rate
        if capitalize_interest:
            balance += interest
            cash_interest = 0.0
        else:
            cash_interest = interest
        # Repayment
        repay = min(repayments[i], balance) if repayments[i] else 0
        balance -= repay
        # Cash debt service = repay + cash_interest
        debt_service = repay + cash_interest
        schedule.append({
            "period": i,
            "drawdown": draw,
            "interest_accrued": interest,
            "interest_cash": cash_interest,
            "interest_capitalized": interest if capitalize_interest else 0,
            "repayment": repay,
            "balance": round(balance, 2),
            "debt_service": debt_service,
        })
    return schedule


def calculate_dscr_series(
    operating_cash_flows: List[float],
    debt_services: List[float],
) -> List[Optional[float]]:
    """DSCR per period = OCF / Debt Service"""
    n = max(len(operating_cash_flows), len(debt_services))
    ocf = (operating_cash_flows + [0]*(n - len(operating_cash_flows)))[:n]
    ds = (debt_services + [0]*(n - len(debt_services)))[:n]
    result = []
    for i in range(n):
        if ds[i] == 0:
            result.append(None if ocf[i] == 0 else float('inf') if ocf[i] > 0 else None)
        else:
            result.append(ocf[i] / ds[i])
    return result


def calculate_interest_coverage(ebit: Optional[float], interest: Optional[float]) -> Optional[float]:
    if ebit is None or interest is None or interest == 0:
        return None
    return ebit / interest


def calculate_debt_yield(noi: Optional[float], debt: Optional[float]) -> Optional[float]:
    """Debt Yield = NOI / Debt"""
    if noi is None or debt is None or debt == 0:
        return None
    return noi / debt * 100


def calculate_facility_headroom(facility_limit: float, drawn: float) -> Dict:
    headroom = facility_limit - drawn
    utilization_pct = (drawn / facility_limit * 100) if facility_limit else None
    return {
        "facility_limit": facility_limit,
        "drawn": drawn,
        "headroom": headroom,
        "utilization_pct": utilization_pct,
        "is_breached": headroom < 0,
    }


def levered_vs_unlevered(
    unlevered_cash_flows: List[float],
    debt_drawdowns: List[float],
    debt_service: List[float],  # repay + interest cash
) -> Dict[str, List[float]]:
    """
    Levered CF = Unlevered CF + Drawdowns - Debt Service
    Unlevered is before financing
    """
    n = max(len(unlevered_cash_flows), len(debt_drawdowns), len(debt_service))
    ul = (unlevered_cash_flows + [0]*(n - len(unlevered_cash_flows)))[:n]
    dd = (debt_drawdowns + [0]*(n - len(debt_drawdowns)))[:n]
    ds = (debt_service + [0]*(n - len(debt_service)))[:n]
    levered = [ul[i] + dd[i] - ds[i] for i in range(n)]
    return {
        "unlevered": ul,
        "drawdowns": dd,
        "debt_service": ds,
        "levered": levered,
    }
