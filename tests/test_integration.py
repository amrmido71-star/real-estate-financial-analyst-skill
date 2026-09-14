"""
Integration test — Full project Mock: Land + Construction + Sales + Collections + Financing
"""
import pytest
from datetime import date
from skill.tools.project_metrics import calculate_gdv, calculate_gdc, calculate_development_margin, calculate_break_even_revenue
from skill.tools.sales_collection import aggregate_monthly_cash
from skill.tools.construction_analysis import generate_s_curve
from skill.tools.financing import build_financing_schedule, levered_vs_unlevered
from skill.tools.cashflow_analysis import analyze_cashflow
from skill.tools.investment_metrics import calculate_irr, calculate_npv, calculate_mirr
from skill.tools.scenario_analysis import run_scenarios

def test_full_project_integration():
    # Project: 100 units @5M =500M GDV
    units = [{"units": 60, "price_per_unit": 4_000_000}, {"units": 40, "price_per_unit": 6_500_000}]
    gdv = calculate_gdv(units)
    assert gdv == 500_000_000  # 240M+260M

    cost_breakdown = {"land": 70_000_000, "construction": 200_000_000, "soft": 30_000_000, "marketing": 20_000_000, "financing": 30_000_000}
    gdc = calculate_gdc(cost_breakdown)
    assert gdc == 350_000_000

    margin = calculate_development_margin(gdv, gdc)
    assert margin == 30.0

    # Break-even revenue at 0% and 20%
    be0 = calculate_break_even_revenue(gdc, 0)
    assert be0 == 350_000_000
    be20 = calculate_break_even_revenue(gdc, 20)
    assert be20 == 437_500_000  # 350/0.8

    # Construction S-curve: 200M over 12 months
    monthly_construction = generate_s_curve(200_000_000, 12, "standard")
    assert sum(monthly_construction) == pytest.approx(200_000_000)
    # Convert to yearly for cash flow: sum per 12
    yearly_construction = [sum(monthly_construction)]  # 1 year simplified

    # Sales: 10 sales @5M avg, with schedule 10/10/40/40?
    sales = []
    for i in range(10):
        sales.append({
            "contracted_value": 5_000_000,
            "sale_date": date(2025, 1, 1),
            "schedule": [
                {"label":"Booking","pct":10,"months_after_sale":0},
                {"label":"Contract","pct":10,"months_after_sale":1},
                {"label":"During","pct":40,"months_after_sale":6},
                {"label":"Handover","pct":40,"months_after_sale":12},
            ]
        })
    monthly_collections = aggregate_monthly_cash(sales, collection_rate=90)
    total_collections = sum(monthly_collections.values())
    # Expected: 10*5M =50M total (90% on-time +10% delayed =100% total, our engine splits not reduces)
    # So total remains 50M, but delayed portion exists
    assert total_collections == pytest.approx(50_000_000, rel=1e-2)
    # Verify that with 90% rate, total still 50M (delayed logic)
    monthly_100 = aggregate_monthly_cash(sales, collection_rate=100)
    assert sum(monthly_100.values()) == pytest.approx(50_000_000, rel=1e-2)

    # Financing: 40% debt =140M
    total_debt = 140_000_000
    sched = build_financing_schedule(total_debt, [0.5,0.5], 0.12, capitalize_interest=True)
    assert sched[0]["drawdown"] == 70_000_000
    assert len(sched) == 2

    # Build Yearly cash flows: Simplified
    # Y0: -land - construction Y0 part + debt draw
    # Y1: collections + debt draw - construction
    cfs_unlevered = [-70_000_000 - 100_000_000, -100_000_000 + 20_000_000, 25_000_000]  # simplified
    # Levered
    drawdowns = [70_000_000, 70_000_000, 0]
    debt_service = [0, 0, 10_000_000]  # simplified
    levered = levered_vs_unlevered(cfs_unlevered, drawdowns, debt_service)
    assert len(levered["levered"]) == 3

    # IRR/NPV on realistic project cash flows
    project_cfs = [-350_000_000, 100_000_000, 200_000_000, 250_000_000]
    irr = calculate_irr(project_cfs)
    npv = calculate_npv(project_cfs, 0.12)
    assert irr is not None
    assert irr > 0.10
    assert npv is not None
    # MIRR
    mirr = calculate_mirr(project_cfs, 0.10, 0.12)
    assert mirr is not None
    assert mirr < irr  # typically MIRR < IRR when reinvest < IRR

    # Scenario: Best/Worst
    base = {"gdv": gdv, "gdc": gdc, "cash_flows": project_cfs, "discount_rate":0.12, "cost_breakdown": cost_breakdown}
    result = run_scenarios(base, {"selling_price_change_pct":8, "construction_cost_change_pct":-7}, {"selling_price_change_pct":-10, "construction_cost_change_pct":15})
    assert result["best"]["profit"] > result["base"]["profit"]
    assert result["worst"]["profit"] < result["base"]["profit"]
    assert result["best"]["npv"] > result["worst"]["npv"]

def test_regression_npv_period_zero():
    from skill.tools.investment_metrics import calculate_npv
    # Period 0 not discounted
    assert calculate_npv([-500, 0, 0], 0.5) == -500
    assert calculate_npv([0, 100], 0.10) == pytest.approx(90.909, abs=0.01)

def test_regression_break_even():
    from skill.tools.project_metrics import calculate_break_even_price
    # area 62000, gdc 1.249B
    assert calculate_break_even_price(1_249_267_500, 62000, 0) == pytest.approx(20149.47, rel=1e-3)
    assert calculate_break_even_price(100, 1000, 100) is None

def test_regression_sensitivity_cashflow():
    from skill.tools.scenario_analysis import run_sensitivity_analysis
    base = {"gdv":500_000_000,"gdc":350_000_000,"cash_flows":[-350_000_000,200000000,200000000],"discount_rate":0.12}
    res = run_sensitivity_analysis(base, "selling_price", [10])
    # Cash flows should be rebuilt, not just KPI
    assert res[0]["cash_flows"][1] == pytest.approx(220_000_000, rel=1e-6)  # 200*1.10
