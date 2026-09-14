"""
portfolio_analysis.py — Multi-project portfolio analytics
"""

from typing import List, Dict, Optional, Tuple
from .investment_metrics import calculate_irr, calculate_npv


def analyze_portfolio(projects: List[Dict]) -> Dict:
    """
    projects: list of dict each with keys:
        {"code","name","gdv","gdc","cash_flows","equity","peak_funding"}
    Returns portfolio summary.
    """
    if not projects:
        return {"error": "No projects provided"}
    total_gdv = sum(p.get("gdv", 0) or 0 for p in projects)
    total_gdc = sum(p.get("gdc", 0) or 0 for p in projects)
    total_profit = total_gdv - total_gdc
    weighted_margin = (total_profit / total_gdv * 100) if total_gdv else None
    total_equity = sum(p.get("equity", 0) or 0 for p in projects)
    total_peak = sum(p.get("peak_funding", 0) or 0 for p in projects)

    # Portfolio IRR: aggregate cash flows (sum per period)
    # Find max periods
    max_len = max(len(p.get("cash_flows", [])) for p in projects if p.get("cash_flows"))
    agg_cfs = [0.0] * max_len if max_len else []
    for p in projects:
        cfs = p.get("cash_flows", [])
        for i, cf in enumerate(cfs):
            agg_cfs[i] += cf
    portfolio_irr = calculate_irr(agg_cfs) if agg_cfs else None
    portfolio_npv = calculate_npv(agg_cfs, 0.15) if agg_cfs else None

    # Ranking
    # By margin
    by_margin = sorted(projects, key=lambda x: ((x.get("gdv",0)-x.get("gdc",0))/x.get("gdv",1)*100 if x.get("gdv") else -999), reverse=True)
    # By peak funding
    by_peak = sorted(projects, key=lambda x: x.get("peak_funding", 0) or 0, reverse=True)
    # By profit
    by_profit = sorted(projects, key=lambda x: (x.get("gdv",0)-x.get("gdc",0)), reverse=True)

    best_project = by_margin[0] if by_margin else None
    highest_risk = by_peak[0] if by_peak else None  # largest funding need
    lowest_margin = by_margin[-1] if by_margin else None

    # Concentration check
    largest_gdv = max(p.get("gdv",0) or 0 for p in projects) if projects else 0
    concentration_pct = (largest_gdv / total_gdv * 100) if total_gdv else 0
    concentration_flag = concentration_pct > 60

    return {
        "project_count": len(projects),
        "total_gdv": total_gdv,
        "total_gdc": total_gdc,
        "total_profit": total_profit,
        "weighted_margin_pct": weighted_margin,
        "total_equity": total_equity,
        "total_peak_funding": total_peak,
        "portfolio_irr": portfolio_irr,
        "portfolio_irr_pct": portfolio_irr*100 if portfolio_irr else None,
        "portfolio_npv": portfolio_npv,
        "aggregate_cash_flows": agg_cfs,
        "ranking": {
            "by_margin": [{"code": p.get("code"), "margin": ((p.get("gdv",0)-p.get("gdc",0))/p.get("gdv",1)*100 if p.get("gdv") else None)} for p in by_margin],
            "by_peak": [{"code": p.get("code"), "peak": p.get("peak_funding")} for p in by_peak],
            "by_profit": [{"code": p.get("code"), "profit": (p.get("gdv",0)-p.get("gdc",0))} for p in by_profit],
        },
        "best_project": best_project.get("code") if best_project else None,
        "highest_cash_need_project": highest_risk.get("code") if highest_risk else None,
        "lowest_margin_project": lowest_margin.get("code") if lowest_margin else None,
        "concentration": {
            "largest_gdv": largest_gdv,
            "largest_pct": concentration_pct,
            "is_concentrated": concentration_flag,
        }
    }
