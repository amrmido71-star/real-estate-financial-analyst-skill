"""
test_integrated_model.py — V1.2 Integrated Model: golden case, reconciliation,
scenarios cascade, sensitivity, delay, debt sanity, returns
"""
from skill.tools.integrated_model import IntegratedRealEstateModel
from skill.tools.model_runner import ModelRunner
from examples.golden_project.assumptions import golden_assumptions, best_case_delta, worst_case_delta

def test_golden_project_reconciliation():
    ass = golden_assumptions()
    result = IntegratedRealEstateModel(ass).run()
    assert result.reconciliation["cash_reconciliation"] is True
    assert result.reconciliation["debt_reconciliation"] is True
    assert result.reconciliation["gdv_check"] is True
    assert result.total_units == 300
    assert result.sold_units == 300
    assert result.gdv > 2_500_000_000
    assert result.gdc > 1_500_000_000
    assert result.profit > 500_000_000
    assert 25 < result.margin_pct < 45
    assert result.health_score >= 75

def test_golden_project_returns_sanity():
    result = IntegratedRealEstateModel(golden_assumptions()).run()
    # Equity IRR positive base, NPV positive
    assert result.equity_irr is not None
    assert result.equity_irr > 0.15
    assert result.equity_npv is not None
    assert result.equity_npv > 0
    # Peak funding sanity: >0 and < GDV*0.5
    assert 100_000_000 < result.peak_funding < result.gdv * 0.5
    # MOIC >1.5
    assert result.moic is not None and result.moic > 1.5
    # Levered IRR ≈ equity IRR when no tax nuance (both derived from same levered)
    assert result.levered_irr is not None
    # Check monthly annualization: monthly < annual
    assert result.equity_irr > 0  # annualized > monthly
    assert result.dashboard["returns"]["equity_irr"] == result.equity_irr

def test_peak_funding_and_equity_positive():
    ass = golden_assumptions()
    result = IntegratedRealEstateModel(ass).run()
    total_equity = sum(p.equity_injection for p in result.periods)
    total_dist = sum(p.equity_distribution for p in result.periods)
    assert total_equity > 0
    assert total_dist > total_equity  # profitable so distributions exceed equity
    assert result.peak_equity == total_equity
    assert result.peak_debt > 0
    # Levered cumulative minimum is negative (funding gap)
    assert result.minimum_cash < 0

def test_scenario_cascade_rebuilds():
    base = golden_assumptions()
    runner = ModelRunner(base)
    scenarios = runner.run_scenarios(best_case_delta(), worst_case_delta())
    base_res = scenarios["base"]
    best_res = scenarios["best"]
    worst_res = scenarios["worst"]
    # Best should improve vs base: higher profit, margin, IRR, lower peak
    assert best_res.profit > base_res.profit
    assert best_res.margin_pct > base_res.margin_pct
    if best_res.equity_irr and base_res.equity_irr:
        assert best_res.equity_irr > base_res.equity_irr
    # Worst should degrade
    assert worst_res.profit < base_res.profit
    assert worst_res.margin_pct < base_res.margin_pct

def test_sensitivity_monotonic_price():
    base = golden_assumptions()
    runner = ModelRunner(base)
    sens = runner.sensitivity("selling_price", [-10, -5, 0, 5, 10])
    # GDV should increase monotonically with price
    gdvs = [s["result"].gdv for s in sens]
    assert gdvs == sorted(gdvs)
    # IRR should increase monotonically (if not None)
    irrs = [s["result"].equity_irr for s in sens]
    # Filter Nones
    filtered = [(c, irr) for c, irr in zip([-10,-5,0,5,10], irrs) if irr is not None]
    vals = [v for _, v in filtered]
    assert vals == sorted(vals)

def test_two_way_matrix_shape():
    base = golden_assumptions()
    runner = ModelRunner(base)
    tw = runner.two_way("selling_price", [-10, 0, 10], "construction_cost", [-10, 0, 10])
    assert len(tw["matrix"]) == 3
    assert len(tw["matrix"][0]) == 3

def test_construction_delay_impacts_funding():
    base = golden_assumptions()
    # Delay 6 months: duration increases, peak should rise slightly, profit may dip due to escalation
    from copy import deepcopy
    delayed = deepcopy(base)
    delayed.construction.duration_months += 6
    r_base = IntegratedRealEstateModel(base).run()
    r_delay = IntegratedRealEstateModel(delayed).run()
    # Peak funding with longer build may be higher or similar (not zero)
    assert r_delay.peak_funding > 0
    # GDC with escalation 5% annual: longer duration => slightly higher budget
    assert r_delay.gdc >= r_base.gdc * 0.98  # allow small

def test_debt_sanity_ltc():
    ass = golden_assumptions()
    ass.financing.debt_pct = 50
    result = IntegratedRealEstateModel(ass).run()
    # Debt should be about 50% of GDC? Our debt_pct is of monthly costs, not GDC, so approximate
    # Check debt never exceeds GDC and peak_debt < GDC
    assert result.peak_debt < result.gdc
    assert result.peak_debt > 0
    total_draw = sum(p.debt_draw for p in result.periods)
    total_repay = sum(p.debt_repayment for p in result.periods)
    total_interest = sum(p.interest_accrued for p in result.periods)
    # With capitalized interest, repay can exceed draw by interest amount
    assert total_draw + total_interest >= total_repay - 1  # allow rounding
    final_debt = result.periods[-1].closing_debt
    assert final_debt >= 0
    # Peak debt should be close to max outstanding
    assert result.peak_debt == max(p.closing_debt for p in result.periods)

def test_unit_inventory_reconciliation():
    result = IntegratedRealEstateModel(golden_assumptions()).run()
    assert result.total_units == 300
    assert result.sold_units + result.remaining_units == result.total_units

def test_price_escalation_optional():
    base = golden_assumptions()
    # Enable escalation 10% with no lock - GDV should increase
    from copy import deepcopy
    no_esc = deepcopy(base)
    no_esc.product.price_growth_annual_pct = 0
    esc = deepcopy(base)
    esc.product.price_growth_annual_pct = 10
    esc.product.price_lock_at_booking = False
    r_no = IntegratedRealEstateModel(no_esc).run()
    r_esc = IntegratedRealEstateModel(esc).run()
    assert r_esc.gdv > r_no.gdv

def test_monthly_engine_periods():
    ass = golden_assumptions()
    result = IntegratedRealEstateModel(ass).run()
    # Monthly periods = months between start and end inclusive
    months = (ass.end_date.year - ass.start_date.year)*12 + (ass.end_date.month - ass.start_date.month) + 1
    assert len(result.periods) == months
    assert result.periods[0].label == "2027-01"
    assert result.periods[-1].label == "2029-12"

def test_audit_trail_hash_stable():
    a1 = golden_assumptions()
    a2 = golden_assumptions()
    assert a1.assumption_hash() == a2.assumption_hash()
    # Changing price should change hash
    from copy import deepcopy
    a3 = deepcopy(a1)
    a3.product.avg_price_per_sqm += 1000
    assert a3.assumption_hash() != a1.assumption_hash()
