import pytest
from skill.tools.financial_statements import (
    analyze_income_statement, analyze_balance_sheet, analyze_cash_flow, calculate_ratios
)

def test_income_statement_basic():
    res = analyze_income_statement(
        revenue=1000000, cogs=600000, opex=150000,
        depreciation=30000, amortization=10000, interest=40000, tax=50000
    )
    assert res["gross_profit"] == 400000
    assert res["gross_margin_pct"] == pytest.approx(40.0)
    assert res["operating_profit"] == 250000  # 400-150
    assert res["ebitda"] == 290000  # 250+30+10
    assert res["ebitda_margin_pct"] == pytest.approx(29.0)
    assert res["ebit"] == 250000  # 290-40
    assert res["ebt"] == 210000  # 250-40
    assert res["net_income"] == 160000  # 210-50
    assert res["net_margin_pct"] == pytest.approx(16.0)

def test_income_statement_missing_revenue():
    res = analyze_income_statement(revenue=None, cogs=600000)
    assert "error" in res

def test_balance_sheet():
    res = analyze_balance_sheet(
        cash=100000, receivables=200000, inventory=300000, ppe=1000000,
        payables=150000, short_term_debt=50000, long_term_debt=500000, equity=900000
    )
    assert res["current_assets"] == 600000  # 100+200+300
    assert res["total_assets"] == 1600000
    assert res["current_liab"] == 200000  # 150+50
    assert res["total_debt"] == 550000
    assert res["working_capital"] == 400000  # 600-200
    assert res["net_debt"] == 450000  # 550-100

def test_cash_flow():
    res = analyze_cash_flow(cfo=300000, cfi=-150000, cff=-50000, capex=100000)
    assert res["free_cash_flow"] == 200000  # 300-100
    assert res["net_change_in_cash"] == 100000  # 300-150-50

def test_ratios():
    income = analyze_income_statement(revenue=1000000, cogs=600000, opex=150000, depreciation=30000, amortization=10000, interest=40000, tax=50000)
    balance = analyze_balance_sheet(cash=100000, receivables=200000, inventory=300000, ppe=1000000, payables=150000, short_term_debt=50000, long_term_debt=500000, equity=900000)
    ratios = calculate_ratios(income, balance)
    assert ratios["current_ratio"] == pytest.approx(3.0)  # 600/200
    assert ratios["quick_ratio"] == pytest.approx(1.5)  # (600-300)/200
    assert ratios["debt_to_equity"] == pytest.approx(0.611, rel=1e-2)  # 550/900
    assert ratios["interest_coverage"] == pytest.approx(6.25)  # 250/40
    assert ratios["roe_pct"] == pytest.approx(17.77, rel=1e-2)  # 160/900
    assert ratios["working_capital"] == 400000
    # AR Days: 200/1000*365=73
    assert ratios["ar_days"] == pytest.approx(73.0, rel=1e-1)

def test_ratios_zero_division():
    income = analyze_income_statement(revenue=0, cogs=0)
    balance = analyze_balance_sheet(cash=0, receivables=0, inventory=0, payables=0, short_term_debt=0, long_term_debt=0, equity=0)
    # Should not crash, just None
    ratios = calculate_ratios(income, balance)
    assert ratios["current_ratio"] is None or ratios["current_ratio"] == 0

def test_income_zero_revenue():
    res = analyze_income_statement(revenue=0, cogs=0)
    assert res["gross_margin_pct"] is None
