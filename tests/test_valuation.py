import pytest
from skill.tools.valuation import (
    calculate_wacc, calculate_cost_of_equity_capm, dcf_valuation,
    calculate_terminal_value_gordon, calculate_terminal_value_exit_cap,
    residual_land_value, comparable_valuation, income_valuation
)

def test_wacc():
    wacc = calculate_wacc(cost_of_equity=0.15, cost_of_debt=0.08, equity_weight=0.6, debt_weight=0.4, tax_rate=0.225)
    # 0.15*0.6 + 0.08*0.775*0.4 =0.09+0.0248=0.1148
    assert wacc == pytest.approx(0.1148, rel=1e-3)

def test_wacc_normalize():
    # Weights not summing to 1 => normalize
    wacc = calculate_wacc(0.15, 0.08, 60, 40, 0.225)
    assert wacc == pytest.approx(0.1148, rel=1e-3)

def test_capm():
    ke = calculate_cost_of_equity_capm(0.04, 1.2, 0.06)
    assert ke == pytest.approx(0.112)

def test_dcf():
    cfs = [-1000, 300, 400, 500]
    res = dcf_valuation(cfs, 0.10)
    # NPV = -1000+272.7+330.6+375.7= -21 approx? Let's compute
    # -1000 +300/1.1 +400/1.21+500/1.331 = -1000+272.73+330.58+375.66=-21.03
    assert res["npv_cash_flows"] == pytest.approx(-21.03, abs=0.5)
    assert res["enterprise_value"] == res["npv_cash_flows"]

def test_dcf_with_terminal():
    cfs = [-1000, 300, 400]
    tv = 2000
    res = dcf_valuation(cfs, 0.10, terminal_value=tv, terminal_year=3)
    # PV terminal =2000/1.331=1502.6
    assert res["pv_terminal"] == pytest.approx(1502.6, abs=1)
    assert res["enterprise_value"] == pytest.approx(res["npv_cash_flows"] + 1502.6, abs=1)

def test_gordon():
    tv = calculate_terminal_value_gordon(500, 0.10, 0.02)
    # 500*1.02/(0.10-0.02)=510/0.08=6375
    assert tv == pytest.approx(6375)
    assert calculate_terminal_value_gordon(500, 0.05, 0.06) is None  # r<=g

def test_exit_cap():
    tv = calculate_terminal_value_exit_cap(1000000, 0.08)
    assert tv == 12500000
    assert calculate_terminal_value_exit_cap(1000000, 0) is None

def test_residual_land():
    res = residual_land_value(gdv=1000000, construction=400000, soft=50000, marketing=30000, developer_profit=200000)
    assert res["residual_land_value"] == 320000  # 1000-400-50-30-200
    assert res["land_as_pct_gdv"] == 32.0

def test_residual_with_pct():
    res = residual_land_value(gdv=1000000, construction=400000, developer_profit_pct_gdv=20)
    assert res["developer_profit"] == 200000
    assert res["residual_land_value"] == 600000 - 200000  # 1000-400-200 =400? Wait construction 400, profit 200 => 400k
    # Actually 1M -400k -200k =400k
    assert res["residual_land_value"] == 400000

def test_comparable():
    comps = [{"price_per_sqm":20000},{"price_per_sqm":22000,"adjustment_pct":5},{"price_per_sqm":21000}]
    res = comparable_valuation(1000, comps)
    # Adjusted: 20000, 23100,21000 => avg 21366
    assert res["avg_comp_price_per_sqm"] == pytest.approx(21366.66, abs=10)
    assert res["value"] == pytest.approx(21366.66*1000, rel=1e-3)
    assert res["comps_used"] == 3

def test_comparable_with_subject_adj():
    comps = [{"price_per_sqm":20000}]
    res = comparable_valuation(500, comps, subject_adjustment_pct=10)
    assert res["final_price_per_sqm"] == 22000
    assert res["value"] == 11000000

def test_income_valuation():
    res = income_valuation(annual_rent=1200000, vacancy_rate_pct=5, operating_expenses=300000, cap_rate=0.08)
    # EGI=1.2M*0.95=1.14M, NOI=840k, Value=10.5M
    assert res["egi"] == 1140000
    assert res["noi"] == 840000
    assert res["value"] == pytest.approx(10500000)
    assert res["noi_margin_pct"] == pytest.approx(73.68, rel=1e-2)

def test_income_zero_cap():
    res = income_valuation(1000000, cap_rate=0)
    assert res["value"] is None
