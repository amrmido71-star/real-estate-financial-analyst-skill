"""model_validation.py — Reconciliation and validation for Integrated Model"""
from typing import Dict, List
from .integrated_model import ModelResult

def validate_reconciliation(result: ModelResult) -> Dict[str, List[str]]:
    errors = []
    warnings = []
    info = []
    recon = result.reconciliation

    if not recon.get("units_check"):
        errors.append("Units reconciliation: Sold + Available != Total")

    if not recon.get("gdv_check"):
        errors.append(f"GDV mismatch: {recon['gdv_vs_sum_units']}")

    if not recon.get("cash_reconciliation"):
        errors.append("Cash reconciliation failed: Opening + Net != Closing")

    if not recon.get("debt_reconciliation"):
        errors.append("Debt reconciliation failed: Opening + Draw + Interest - Repayment != Closing")

    # Check for large funding gap
    if result.peak_funding > result.gdv * 0.5:
        warnings.append(f"Peak funding {result.peak_funding:,.0f} >50% GDV — high leverage/funding risk")

    # Check health
    if result.health_score < 40:
        warnings.append(f"Health score {result.health_score} Critical — review assumptions")

    # Check IRR sanity
    if result.equity_irr is not None and result.equity_irr < 0:
        warnings.append(f"Equity IRR negative {result.equity_irr:.1%} — project destroys value at current assumptions")

    # Check missing periods
    if len(result.periods) < 12:
        info.append("Model has <12 months — short timeline, verify end_date")

    return {"errors": errors, "warnings": warnings, "info": info, "is_valid": len(errors)==0}  # type: ignore[dict-item]

def audit_trail(result: ModelResult) -> Dict:
    return {
        "run_id": result.run_id,
        "timestamp": result.timestamp,
        "assumption_hash": result.assumptions.assumption_hash(),
        "assumptions": result.assumptions.to_dict(),
        "currency": result.assumptions.currency,
        "period_range": f"{result.periods[0].label} → {result.periods[-1].label}" if result.periods else None,
        "model_version": "1.2.0",
        "scenario": "base",  # could be extended
    }
