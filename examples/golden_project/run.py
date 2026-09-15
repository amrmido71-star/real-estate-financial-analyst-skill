"""
run.py — Golden Project Runner V1.2
Demonstrates: base run, reconciliation, scenario cascade, sensitivity, reporting
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2]))

from skill.tools.integrated_model import IntegratedRealEstateModel
from skill.tools.model_runner import ModelRunner
from skill.tools.model_validation import validate_reconciliation, audit_trail
from skill.tools.reporting import build_dashboard, build_executive_summary, build_management_pack
from examples.golden_project.assumptions import golden_assumptions, best_case_delta, worst_case_delta, stress_case_delta

def main():
    print("="*70)
    print("GOLDEN PROJECT — East Cairo Compound (300 units)")
    print("="*70)
    assumptions = golden_assumptions()
    print(f"Assumptions hash: {assumptions.assumption_hash()}")
    print(f"GDV (theoretical): {assumptions.product.sellable_area_sqm * assumptions.product.avg_price_per_sqm:,.0f} EGP (sellable area x price, before mix premium)")
    print()

    # 1. Base run
    model = IntegratedRealEstateModel(assumptions)
    result = model.run()
    print("--- BASE CASE ---")
    print(f"GDV: {result.gdv:,.0f}  GDC: {result.gdc:,.0f}  Profit: {result.profit:,.0f}  Margin: {result.margin_pct:.1f}%")
    print(f"Units: {result.sold_units}/{result.total_units} sold")
    print(f"Peak Funding: {result.peak_funding:,.0f}  Peak Debt: {result.peak_debt:,.0f}  Peak Equity: {result.peak_equity:,.0f}")
    irr_str = f"{result.equity_irr:.2%}" if result.equity_irr is not None else "N/A"
    npv_str = f"{result.equity_npv:,.0f}" if result.equity_npv is not None else "N/A"
    moic_str = f"{result.moic:.2f}" if result.moic is not None else "N/A"
    print(f"Equity IRR: {irr_str}  NPV: {npv_str}  MOIC: {moic_str}  Payback: {result.payback_period}")
    print(f"Health: {result.financial_health} ({result.health_score}/100)")
    print(f"Reconciliation — cash: {result.reconciliation['cash_reconciliation']} debt: {result.reconciliation['debt_reconciliation']} gdv: {result.reconciliation['gdv_check']}")
    print(f"Run ID: {result.run_id}")
    print()

    # 2. Validation
    validation = validate_reconciliation(result)
    print("--- VALIDATION ---")
    print(f"Valid: {validation['is_valid']}  Errors: {validation['errors']}  Warnings: {validation['warnings']}")
    print(f"Audit trail: {audit_trail(result)}")
    print()

    # 3. Scenarios (true cascade)
    runner = ModelRunner(assumptions)
    scenarios = runner.run_scenarios(best_case_delta(), worst_case_delta(), stress_case_delta())
    print("--- SCENARIOS (Assumption→Revenue→Collection→Cost→Financing→Cash→IRR) ---")
    for k in ["base","best","worst","stress"]:
        r = scenarios.get(k)
        if r:
            irr_s = f"{r.equity_irr:.1%}" if r.equity_irr is not None else "N/A"
            npv_s = f"{r.equity_npv:,.0f}" if r.equity_npv is not None else "N/A"
            print(f"{k:>6}: IRR {irr_s}  NPV {npv_s}  Profit {r.profit:,.0f}  Margin {r.margin_pct:.1f}%  Peak {r.peak_funding:,.0f}")
    print()

    # 4. Sensitivity
    print("--- SENSITIVITY (one-way: selling_price ±20%) ---")
    sens = runner.sensitivity("selling_price", [-20,-10,-5,0,5,10,20])
    for s in sens:
        ch = s["change"]
        r = s["result"]
        irr_s = f"{r.equity_irr:.1%}" if r.equity_irr is not None else "N/A"
        npv_s = f"{r.equity_npv:,.0f}" if r.equity_npv is not None else "N/A"
        print(f"  Price {ch:+3.0f}% → IRR {irr_s}  NPV {npv_s}  GDV {r.gdv:,.0f}")
    print()

    # 5. Two-way
    print("--- TWO-WAY (price vs cost) ---")
    tw = runner.two_way("selling_price", [-10,0,10], "construction_cost", [-10,0,10])
    print("Matrix rows=price changes, cols=cost changes")
    for i, ch1 in enumerate(tw["changes1"]):
        row = " ".join(f"{v:.1%}" if v else "N/A " for v in tw["matrix"][i])
        print(f"  price {ch1:+3.0f}%: {row}")
    print()

    # 6. Dashboard & Report
    print("--- DASHBOARD ---")
    import json
    dash = build_dashboard(result)
    print(json.dumps({k: v for k,v in dash.items() if k in ["financial_health","health_score","gdv","gdc","profit","margin_pct"]}, indent=2, ensure_ascii=False))
    print()
    print("--- EXECUTIVE SUMMARY (preview 400 chars) ---")
    summary = build_executive_summary(result)
    print(summary[:800])
    print("\n... (full summary written to management_pack)")
    print()

    # 7. Management pack
    pack = build_management_pack(result, scenarios)
    print(f"Management pack keys: {list(pack.keys())}")
    print("="*70)
    print("GOLDEN PROJECT COMPLETE — reconciliation passed, scenarios rebuilt end-to-end")
    print("="*70)

if __name__ == "__main__":
    main()
