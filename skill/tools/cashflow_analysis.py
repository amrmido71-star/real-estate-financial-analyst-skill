"""
cashflow_analysis.py — Cash Flow Forecasting & Liquidity Analysis
"""

from typing import Optional, List, Dict, Tuple


def calculate_cumulative_cashflow(
    net_cash_flows: List[float], opening_cash: float = 0
) -> List[float]:
    """Cumulative = Opening + running sum of Net CFs"""
    cumulative = []
    running = opening_cash
    for cf in net_cash_flows:
        running += cf
        cumulative.append(running)
    return cumulative


def calculate_peak_funding(cumulative_cash_flows: List[float], opening_cash: float = 0) -> Optional[Dict]:
    """
    Peak Funding Requirement = minimum cumulative (most negative) — the max cash needed.
    Returns dict: {"peak_amount": float, "peak_period": int, "peak_cumulative": float}
    peak_amount is positive number representing funding needed.
    If never negative, peak is 0 (no funding needed).
    """
    if not cumulative_cash_flows:
        return None
    min_val = min(cumulative_cash_flows)
    min_idx = cumulative_cash_flows.index(min_val)
    # Funding needed is how far below opening/zero we go
    # If cumulative is absolute cash balance, peak funding = max(0, -min_val) if opening included?
    # Here cumulative already includes opening, so negative balance means need funding.
    peak_amount = abs(min_val) if min_val < 0 else 0.0
    return {
        "peak_amount": peak_amount,
        "peak_period": min_idx,
        "peak_cumulative": min_val,
    }


def calculate_net_cashflow(
    inflows: List[float], outflows: List[float], financing: Optional[List[float]] = None
) -> List[float]:
    """
    Net CF = Inflows - Outflows + Financing (financing can be positive draw or negative repayment)
    All lists must be same length; pads with 0 if needed.
    """
    n = max(len(inflows or []), len(outflows or []), len(financing or []) if financing else 0)
    if n == 0:
        return []
    # Pad
    inf = (inflows or []) + [0] * (n - len(inflows or []))
    out = (outflows or []) + [0] * (n - len(outflows or []))
    fin = (financing or [0] * n) if financing else [0] * n
    if len(fin) < n:
        fin = fin + [0] * (n - len(fin))
    return [inf[i] - out[i] + fin[i] for i in range(n)]


def calculate_free_cashflow(operating_cf: List[float], development_cf: List[float]) -> List[float]:
    """FCF = Operating CF + Development CF (both can be negative for development)"""
    n = max(len(operating_cf), len(development_cf))
    op = operating_cf + [0] * (n - len(operating_cf))
    dev = development_cf + [0] * (n - len(development_cf))
    return [op[i] + dev[i] for i in range(n)]


def calculate_dscr(operating_cashflow: Optional[float], debt_service: Optional[float]) -> Optional[float]:
    """DSCR = Operating CF / Debt Service"""
    if operating_cashflow is None or debt_service is None or debt_service == 0:
        return None
    return operating_cashflow / debt_service


def calculate_runway(cash_balance: Optional[float], avg_monthly_burn: Optional[float]) -> Optional[float]:
    """Runway (months) = Cash Balance / Avg Monthly Burn (burn should be positive number)"""
    if cash_balance is None or avg_monthly_burn is None or avg_monthly_burn == 0:
        return None
    return cash_balance / abs(avg_monthly_burn)


def calculate_collection_metrics(
    contracted: Optional[float], collected: Optional[float], due: Optional[float]
) -> Dict[str, Optional[float]]:
    """Collection metrics bundle"""
    outstanding = None
    if contracted is not None and collected is not None:
        outstanding = contracted - collected
    efficiency = None
    if collected is not None and due is not None and due != 0:
        efficiency = (collected / due) * 100
    overdue = None
    if due is not None and collected is not None:
        overdue = due - collected  # Amount due but not collected
        if overdue is not None and overdue < 0:
            overdue = 0
    return {
        "outstanding_receivables": outstanding,
        "collection_efficiency_pct": efficiency,
        "overdue_amount": overdue,
    }


def analyze_cashflow(
    inflows: List[float],
    outflows: List[float],
    financing: Optional[List[float]] = None,
    opening_cash: float = 0,
    period_labels: Optional[List[str]] = None,
) -> Dict:
    """
    Full cash flow analysis: Net, Cumulative, Peak Funding, Summary
    """
    net = calculate_net_cashflow(inflows, outflows, financing)
    cumulative = calculate_cumulative_cashflow(net, opening_cash)
    peak = calculate_peak_funding(cumulative)

    total_inflows = sum(inflows) if inflows else 0
    total_outflows = sum(outflows) if outflows else 0
    total_financing = sum(financing) if financing else 0
    total_net = sum(net) if net else 0
    closing_cash = cumulative[-1] if cumulative else opening_cash

    return {
        "periods": len(net),
        "period_labels": period_labels or [f"P{i+1}" for i in range(len(net))],
        "inflows": inflows,
        "outflows": outflows,
        "financing": financing or [0] * len(net),
        "net_cashflow": net,
        "cumulative_cashflow": cumulative,
        "opening_cash": opening_cash,
        "closing_cash": closing_cash,
        "total_inflows": total_inflows,
        "total_outflows": total_outflows,
        "total_financing": total_financing,
        "total_net": total_net,
        "peak_funding": peak,
    }


def validate_cashflow_sequence(cumulative: List[float]) -> List[str]:
    """Check cumulative logic — returns list of warnings"""
    warnings = []
    for i in range(1, len(cumulative)):
        # No specific rule but flag large drops
        change = cumulative[i] - cumulative[i - 1]
        if abs(change) > 1e9:
            warnings.append(f"Period {i+1}: unusually large cash movement: {change:,.0f}")
    return warnings
