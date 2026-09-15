"""reporting.py — Management Pack & Dashboard from ModelResult"""
from typing import Dict, List
from .integrated_model import ModelResult

def build_dashboard(result: ModelResult) -> Dict:
    return result.dashboard

def build_executive_summary(result: ModelResult) -> str:
    a = result.assumptions
    health = result.financial_health
    score = result.health_score
    # Determine decision
    hurdle = a.hurdle_rate_annual_pct/100
    irr = result.equity_irr or 0
    if irr is None:
        decision = "Not Recommended (Insufficient Data)"
    elif irr < hurdle - 0.03:
        decision = "Not Recommended"
    elif irr < hurdle:
        decision = "Conditionally Recommended"
    elif irr < hurdle + 0.03:
        decision = "Watchlist"
    else:
        decision = "Recommended"

    reasons = []
    if irr is not None:
        reasons.append(f"Equity IRR {irr:.1%} vs Hurdle {hurdle:.1%}")
    reasons.append(f"GDV {result.gdv:,.0f} / GDC {result.gdc:,.0f} / Profit {result.profit:,.0f} / Margin {result.margin_pct:.1f}%")
    reasons.append(f"Peak Funding {result.peak_funding:,.0f} / Peak Debt {result.peak_debt:,.0f}")
    if result.minimum_cash < 0:
        reasons.append(f"Minimum Cash {result.minimum_cash:,.0f} (funding gap)")
    if not result.reconciliation.get("cash_reconciliation"):
        reasons.append("Cash reconciliation failed — review model")

    # Risks linked to numbers
    risks = []
    if result.margin_pct < 15:
        risks.append(f"Margin {result.margin_pct:.1f}% <15% — low buffer")
    if result.peak_funding > result.gdv * 0.4:
        risks.append(f"Peak funding {result.peak_funding/result.gdv:.1%} of GDV — high leverage")
    if a.collections.collection_rate_pct < 85:
        risks.append(f"Collection rate {a.collections.collection_rate_pct}% <85%")

    irr_str = f"{irr:.1%}" if irr else "N/A"
    npv_val = result.equity_npv
    npv_str = f"{npv_val:,.0f}" if npv_val is not None else "N/A"
    moic_str = f"{result.moic:.2f}" if result.moic else "N/A"
    payback_str = f"{result.payback_period:.1f}" if result.payback_period else "N/A"
    summary = f"""# Executive Summary — {a.project_name} ({result.run_id})

**Financial Health:** {health} (Score {score}/100)
**Investment Decision:** {decision}

**Reasons:**
""" + "\n".join(f"- {r}" for r in reasons) + f"""

**Key Metrics:**
- GDV: {result.gdv:,.0f} {a.currency}
- GDC: {result.gdc:,.0f}
- Profit: {result.profit:,.0f} / Margin {result.margin_pct:.1f}% / On Cost {result.profit_on_cost_pct:.1f}%
- Equity IRR: {irr_str} / NPV: {npv_str}
- MOIC: {moic_str} / Payback: {payback_str} periods
- Peak Funding: {result.peak_funding:,.0f} / Minimum Cash: {result.minimum_cash:,.0f}

**Risks:**
""" + ("\n".join(f"- {r}" for r in risks) if risks else "- No critical risks") + """

**Recommendations:**
- Review assumptions with health <60
- Prioritize collection delays if collection <85%
- Stress test price -10% and cost +15% before decision
"""
    return summary

def build_management_pack(result: ModelResult, scenarios: Dict = None, sensitivity: List = None) -> Dict:
    """Structured pack for reporting layer — does NOT recalculate, uses result directly"""
    pack = {
        "executive_summary": build_executive_summary(result),
        "project_kpis": {
            "gdv": result.gdv,
            "gdc": result.gdc,
            "profit": result.profit,
            "margin_pct": result.margin_pct,
            "profit_on_cost_pct": result.profit_on_cost_pct,
            "total_units": result.total_units,
            "sold_units": result.sold_units,
        },
        "sales_performance": result.dashboard["sales"],
        "collections": result.dashboard["collections"],
        "construction": result.dashboard["construction"],
        "cashflow": result.dashboard["cashflow"],
        "financing": {
            "peak_debt": result.peak_debt,
            "peak_equity": result.peak_equity,
            "equity_invested": sum(p.equity_injection for p in result.periods),
        },
        "returns": result.dashboard["returns"],
        "reconciliation": result.reconciliation,
        "risks": [],  # to be filled by risk engine
        "scenarios": scenarios,
        "sensitivity": sensitivity,
        "audit_trail": {
            "run_id": result.run_id,
            "timestamp": result.timestamp,
            "assumption_hash": result.assumptions.assumption_hash(),
        }
    }
    return pack
