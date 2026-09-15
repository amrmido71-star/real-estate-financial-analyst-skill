import pytest
from skill.tools.construction_analysis import (
    calculate_eac, calculate_etc, calculate_variance, classify_cost_variance,
    generate_s_curve, analyze_construction, monthly_progress_report
)

def test_eac_etc():
    assert calculate_eac(60, 40) == 100
    assert calculate_etc(100, 60) == 40
    assert calculate_etc(100, 60, re_estimate=50) == 50

def test_variance():
    var_abs, var_pct = calculate_variance(100, 112)
    assert var_abs == -12  # Budget - Actual = 100-112 = -12
    assert var_pct == -12.0
    # Under budget
    var_abs2, var_pct2 = calculate_variance(100, 90)
    assert var_abs2 == 10
    assert var_pct2 == 10.0

def test_classify():
    assert classify_cost_variance(100, 112) == "Unfavorable"
    assert classify_cost_variance(100, 90) == "Favorable"
    assert classify_cost_variance(100, 101) == "Neutral"  # 1% <2% neutral
    assert classify_cost_variance(100, 105) == "Unfavorable"  # 5%

def test_s_curve_standard():
    monthly = generate_s_curve(1200000, 12, "standard")
    assert len(monthly) == 12
    assert sum(monthly) == pytest.approx(1200000, rel=1e-6)
    # S-curve: middle months higher than start/end
    assert monthly[5] > monthly[0]
    assert monthly[5] > monthly[11]

def test_s_curve_linear():
    monthly = generate_s_curve(1200000, 12, "linear")
    assert all(v == pytest.approx(100000) for v in monthly)

def test_s_curve_front_back():
    front = generate_s_curve(1000000, 10, "front_loaded")
    back = generate_s_curve(1000000, 10, "back_loaded")
    assert sum(front) == pytest.approx(1000000)
    assert sum(back) == pytest.approx(1000000)
    # Front loaded should have more early
    assert front[0] > back[0]

def test_analyze_construction_overrun():
    res = analyze_construction(budget=1000000, actual=600000, etc=500000, pct_complete=50)
    assert res["eac"] == 1100000
    assert res["variance_budget_vs_eac_abs"] == -100000
    assert res["classification_eac"] == "Unfavorable"
    assert res["overrun_risk"]

def test_analyze_construction_on_track():
    res = analyze_construction(budget=1000000, actual=500000, etc=500000, pct_complete=50)
    assert res["eac"] == 1000000
    assert res["classification_eac"] == "Neutral"

def test_monthly_progress():
    budget = [100,100,100,100]
    actual = [110,90,105,95]
    report = monthly_progress_report(budget, actual, labels=["M1","M2","M3","M4"])
    assert len(report) == 4
    assert report[0]["variance_abs"] == -10
    assert report[0]["cumulative_actual"] == 110
    assert report[3]["cumulative_budget"] == 400
    assert report[3]["cumulative_actual"] == 400

def test_s_curve_zero_months():
    assert generate_s_curve(1000000, 0) == []
