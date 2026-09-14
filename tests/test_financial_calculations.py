import pytest
from skill.tools.financial_calculations import (
    calculate_gross_profit,
    calculate_gross_margin,
    calculate_operating_profit,
    calculate_ebitda,
    calculate_ebit,
    calculate_net_profit,
    calculate_net_margin,
    calculate_variance,
    calculate_variance_pct,
    classify_variance,
    calculate_roi,
    calculate_break_even_sales,
    vertical_analysis,
    horizontal_analysis,
)


def test_gross_profit():
    assert calculate_gross_profit(100, 60) == 40
    assert calculate_gross_profit(None, 60) is None
    assert calculate_gross_profit(100, None) is None


def test_gross_margin():
    assert calculate_gross_margin(100, 60) == 40.0
    assert calculate_gross_margin(200, 120) == 40.0
    assert calculate_gross_margin(0, 60) is None
    assert calculate_gross_margin(None, 60) is None
    assert calculate_gross_margin(100, None) is None
    # Negative margin
    assert calculate_gross_margin(100, 120) == -20.0


def test_operating_profit():
    assert calculate_operating_profit(40, 15) == 25
    assert calculate_operating_profit(None, 15) is None


def test_ebitda():
    assert calculate_ebitda(25, 5, 2) == 32
    assert calculate_ebitda(25, 0, 0) == 25
    assert calculate_ebitda(None, 5, 2) is None
    assert calculate_ebitda(10) == 10  # default depreciation 0


def test_ebit():
    assert calculate_ebit(32, 5, 2) == 25
    assert calculate_ebit(30, 5) == 25


def test_net_profit():
    assert calculate_net_profit(25, 5, 5) == 15
    assert calculate_net_profit(None, 5, 5) is None
    assert calculate_net_profit(20) == 20


def test_net_margin():
    assert calculate_net_margin(15, 100) == 15.0
    assert calculate_net_margin(15, 0) is None
    assert calculate_net_margin(None, 100) is None


def test_variance():
    assert calculate_variance(112, 100) == 12
    assert calculate_variance(90, 100) == -10
    assert calculate_variance(None, 100) is None


def test_variance_pct():
    assert calculate_variance_pct(112, 100) == 12.0
    assert calculate_variance_pct(90, 100) == -10.0
    assert calculate_variance_pct(100, 0) is None
    assert calculate_variance_pct(None, 100) is None
    # Budget negative handling
    assert calculate_variance_pct(90, -100) == pytest.approx(190.0)


def test_classify_variance_revenue():
    # Revenue: actual > budget => Favorable
    assert classify_variance(110, 100, is_revenue=True) == "Favorable"
    assert classify_variance(90, 100, is_revenue=True) == "Unfavorable"
    # Neutral within 2%
    assert classify_variance(101, 100, is_revenue=True, neutral_threshold_pct=2.0) == "Neutral"
    assert classify_variance(101.9, 100, is_revenue=True) == "Neutral"
    assert classify_variance(102.1, 100, is_revenue=True) == "Favorable"


def test_classify_variance_cost():
    # Cost: actual > budget => Unfavorable
    assert classify_variance(112, 100, is_revenue=False) == "Unfavorable"
    assert classify_variance(90, 100, is_revenue=False) == "Favorable"
    assert classify_variance(101, 100, is_revenue=False, neutral_threshold_pct=2.0) == "Neutral"


def test_classify_variance_zero_budget():
    assert classify_variance(10, 0, is_revenue=True) == "Favorable"
    assert classify_variance(0, 0, is_revenue=True) == "Neutral"
    assert classify_variance(None, 100) == "N/A"


def test_roi():
    assert calculate_roi(150, 100) == 50.0
    assert calculate_roi(80, 100) == -20.0
    assert calculate_roi(150, 0) is None
    assert calculate_roi(None, 100) is None


def test_break_even_sales():
    assert calculate_break_even_sales(100_000, 0.4) == 250_000
    assert calculate_break_even_sales(100_000, 0) is None
    assert calculate_break_even_sales(None, 0.4) is None


def test_vertical_analysis():
    assert vertical_analysis(30, 100) == 30.0
    assert vertical_analysis(30, 0) is None


def test_horizontal_analysis():
    abs_c, pct = horizontal_analysis(120, 100)
    assert abs_c == 20
    assert pct == 20.0
    abs_c, pct = horizontal_analysis(80, 100)
    assert pct == -20.0
    result = horizontal_analysis(50, 0)
    assert result[1] is None
    assert horizontal_analysis(None, 100) is None


def test_example_financials_q2():
    # Q2 Actual vs Budget from example_financials.csv
    # Q2 2025: Revenue 64M, COR 43.5M, Budget 60M / 39M
    revenue_actual = 64_000_000
    cor_actual = 43_500_000
    revenue_budget = 60_000_000
    cor_budget = 39_000_000

    gross_actual = calculate_gross_profit(revenue_actual, cor_actual)
    assert gross_actual == 20_500_000

    margin_actual = calculate_gross_margin(revenue_actual, cor_actual)
    assert margin_actual == pytest.approx(32.03125, rel=1e-4)

    margin_budget = calculate_gross_margin(revenue_budget, cor_budget)
    assert margin_budget == pytest.approx(35.0)

    # Variance: Construction Budget 100M, Actual 112M example from spec
    var = calculate_variance(112_000_000, 100_000_000)
    var_pct = calculate_variance_pct(112_000_000, 100_000_000)
    assert var == 12_000_000
    assert var_pct == 12.0
    assert classify_variance(112_000_000, 100_000_000, is_revenue=False) == "Unfavorable"
