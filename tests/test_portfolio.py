import pytest
from skill.tools.portfolio_analysis import analyze_portfolio

def test_portfolio_basic():
    projects = [
        {"code":"A","name":"Project A","gdv":500000000,"gdc":350000000,"cash_flows":[-350000000,200000000,200000000],"equity":150000000,"peak_funding":100000000},
        {"code":"B","name":"Project B","gdv":800000000,"gdc":600000000,"cash_flows":[-600000000,300000000,400000000],"equity":200000000,"peak_funding":200000000},
    ]
    res = analyze_portfolio(projects)
    assert res["total_gdv"] == 1300000000
    assert res["total_gdc"] == 950000000
    assert res["total_profit"] == 350000000
    assert res["weighted_margin_pct"] == pytest.approx(26.923, rel=1e-2)
    assert res["project_count"] == 2
    assert res["total_peak_funding"] == 300000000
    assert res["portfolio_irr"] == pytest.approx(0.1003, abs=0.001)
    assert res["best_project"] == "A"
    assert "ranking" in res

def test_portfolio_concentration():
    projects = [
        {"code":"A","gdv":900000000,"gdc":600000000,"cash_flows":[-100,200],"peak_funding":100},
        {"code":"B","gdv":100000000,"gdc":80_000_000,"cash_flows":[-80,100],"peak_funding":50},
    ]
    res = analyze_portfolio(projects)
    assert res["concentration"]["largest_pct"] == 90.0
    assert res["concentration"]["is_concentrated"]

def test_portfolio_single():
    projects = [
        {"code":"A","gdv":500000000,"gdc":400000000,"cash_flows":[-400000000,150000000,350000000],"peak_funding":120000000},
    ]
    res = analyze_portfolio(projects)
    assert res["total_gdv"] == 500000000
    assert res["best_project"] == "A"
    assert res["lowest_margin_project"] == "A"

def test_portfolio_empty():
    res = analyze_portfolio([])
    assert "error" in res

def test_portfolio_ranking():
    projects = [
        {"code":"A","gdv":1000000,"gdc":800000,"cash_flows":[-800000,300000],"peak_funding":50000},  # margin 20%
        {"code":"B","gdv":1000000,"gdc":600000,"cash_flows":[-600000,500000],"peak_funding":100000}, # margin 40%
        {"code":"C","gdv":1000000,"gdc":900000,"cash_flows":[-900000,200000],"peak_funding":200000}, # margin 10%
    ]
    res = analyze_portfolio(projects)
    assert res["best_project"] == "B"  # highest margin
    assert res["lowest_margin_project"] == "C"
    assert res["highest_cash_need_project"] == "C"  # largest peak
