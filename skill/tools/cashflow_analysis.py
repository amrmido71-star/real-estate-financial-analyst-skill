"""
cashflow_analysis.py — Cash Flow Forecasting & Liquidity Analysis
Enhanced: supports Monthly/Quarterly/Annual, detailed breakdown, peak funding, DSCR, runway
"""

from typing import Optional, List, Dict
from datetime import date
from .models import CashFlowPeriod


def calculate_cumulative_cashflow(net_cash_flows: List[float], opening_cash: float = 0) -> List[float]:
    cumulative = []
    running = opening_cash
    for cf in net_cash_flows:
        running += cf
        cumulative.append(running)
    return cumulative


def calculate_peak_funding(cumulative_cash_flows: List[float], opening_cash: float = 0) -> Optional[Dict]:
    if not cumulative_cash_flows:
        return None
    min_val = min(cumulative_cash_flows)
    min_idx = cumulative_cash_flows.index(min_val)
    peak_amount = abs(min_val) if min_val < 0 else 0.0
    return {
        "peak_amount": peak_amount,
        "peak_period": min_idx,
        "peak_cumulative": min_val,
        "minimum_cash": min_val,
    }


def calculate_net_cashflow(inflows: List[float], outflows: List[float], financing: Optional[List[float]] = None) -> List[float]:
    n = max(len(inflows or []), len(outflows or []), len(financing or []) if financing else 0)
    if n == 0:
        return []
    inf = (inflows or []) + [0] * (n - len(inflows or []))
    out = (outflows or []) + [0] * (n - len(outflows or []))
    fin = (financing or [0] * n) if financing else [0] * n
    if len(fin) < n:
        fin = fin + [0] * (n - len(fin))
    return [inf[i] - out[i] + fin[i] for i in range(n)]


def calculate_free_cashflow(operating_cf: List[float], development_cf: List[float]) -> List[float]:
    n = max(len(operating_cf), len(development_cf))
    op = operating_cf + [0] * (n - len(operating_cf))
    dev = development_cf + [0] * (n - len(development_cf))
    return [op[i] + dev[i] for i in range(n)]


def calculate_dscr(operating_cashflow: Optional[float], debt_service: Optional[float]) -> Optional[float]:
    if operating_cashflow is None or debt_service is None or debt_service == 0:
        return None
    return operating_cashflow / debt_service


def calculate_runway(cash_balance: Optional[float], avg_monthly_burn: Optional[float]) -> Optional[float]:
    if cash_balance is None or avg_monthly_burn is None or avg_monthly_burn == 0:
        return None
    return cash_balance / abs(avg_monthly_burn)


def calculate_collection_metrics(contracted: Optional[float], collected: Optional[float], due: Optional[float]) -> Dict[str, Optional[float]]:
    outstanding = None
    if contracted is not None and collected is not None:
        outstanding = contracted - collected
    efficiency = None
    if collected is not None and due is not None and due != 0:
        efficiency = (collected / due) * 100
    overdue = None
    if due is not None and collected is not None:
        overdue = due - collected
        if overdue is not None and overdue < 0:
            overdue = 0
    return {
        "outstanding_receivables": outstanding,
        "collection_efficiency_pct": efficiency,
        "overdue_amount": overdue,
    }


def build_detailed_cashflow(
    periods: List[CashFlowPeriod],
    opening_cash: float = 0,
    period_type: str = "monthly",  # monthly, quarterly, annual
) -> Dict:
    """
    Build cash flow from typed CashFlowPeriod objects.
    Supports period_type for annualization and reporting.
    """
    net = [p.net for p in periods]
    cumulative = calculate_cumulative_cashflow(net, opening_cash)
    peak = calculate_peak_funding(cumulative)

    total_inflows = sum(p.total_inflows for p in periods)
    total_outflows = sum(p.total_outflows for p in periods)
    total_net = sum(net)
    closing = cumulative[-1] if cumulative else opening_cash

    # Operating vs Development vs Financing split
    operating_inflows = sum(p.inflows_collections for p in periods)
    development_outflows = sum(p.outflows_construction + p.outflows_soft for p in periods)
    financing_net = sum(p.inflows_financing - p.outflows_financing for p in periods)

    # Minimum cash and funding gap
    min_cash = min(cumulative) if cumulative else opening_cash
    funding_gap = abs(min_cash) if min_cash < 0 else 0

    return {
        "period_type": period_type,
        "periods": len(periods),
        "periods_detail": periods,
        "net_cashflow": net,
        "cumulative_cashflow": cumulative,
        "opening_cash": opening_cash,
        "closing_cash": closing,
        "total_inflows": total_inflows,
        "total_outflows": total_outflows,
        "total_net": total_net,
        "operating_inflows": operating_inflows,
        "development_outflows": development_outflows,
        "financing_net": financing_net,
        "peak_funding": peak,
        "minimum_cash": min_cash,
        "funding_gap": funding_gap,
    }


def analyze_cashflow(
    inflows: List[float],
    outflows: List[float],
    financing: Optional[List[float]] = None,
    opening_cash: float = 0,
    period_labels: Optional[List[str]] = None,
    period_type: str = "monthly",
) -> Dict:
    net = calculate_net_cashflow(inflows, outflows, financing)
    cumulative = calculate_cumulative_cashflow(net, opening_cash)
    peak = calculate_peak_funding(cumulative)
    total_inflows = sum(inflows) if inflows else 0
    total_outflows = sum(outflows) if outflows else 0
    total_financing = sum(financing) if financing else 0
    total_net = sum(net) if net else 0
    closing_cash = cumulative[-1] if cumulative else opening_cash
    # Additional metrics
    min_cash = min(cumulative) if cumulative else opening_cash
    funding_gap = abs(min_cash) if min_cash < 0 else 0
    return {
        "period_type": period_type,
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
        "minimum_cash": min_cash,
        "funding_gap": funding_gap,
    }


def aggregate_to_quarterly(monthly_net: List[float]) -> List[float]:
    """Aggregate monthly net cash flows to quarterly"""
    quarterly = []
    for i in range(0, len(monthly_net), 3):
        quarterly.append(sum(monthly_net[i:i+3]))
    return quarterly


def aggregate_to_annual(monthly_net: List[float]) -> List[float]:
    annual = []
    for i in range(0, len(monthly_net), 12):
        annual.append(sum(monthly_net[i:i+12]))
    return annual


def validate_cashflow_sequence(cumulative: List[float]) -> List[str]:
    warnings = []
    for i in range(1, len(cumulative)):
        change = cumulative[i] - cumulative[i - 1]
        if abs(change) > 1e9:
            warnings.append(f"Period {i+1}: unusually large cash movement: {change:,.0f}")
    return warnings
