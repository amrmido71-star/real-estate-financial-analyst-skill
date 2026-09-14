import pytest
from skill.tools.financing import (
    calculate_ltc, calculate_ltv, calculate_debt_to_equity,
    build_financing_schedule, calculate_dscr_series, calculate_interest_coverage,
    calculate_debt_yield, calculate_facility_headroom, levered_vs_unlevered
)

def test_ltc_ltv():
    assert calculate_ltc(60, 100) == 60.0
    assert calculate_ltv(60, 100) == 60.0
    assert calculate_ltc(60, 0) is None
    assert calculate_ltv(60, 0) is None

def test_debt_to_equity():
    assert calculate_debt_to_equity(60, 40) == 1.5
    assert calculate_debt_to_equity(60, 0) is None

def test_financing_schedule_capitalized():
    sched = build_financing_schedule(
        total_debt=1000000,
        drawdown_schedule=[500000, 500000],
        interest_rate_annual=0.12,
        repayment_schedule=[0,0],
        capitalize_interest=True
    )
    assert len(sched) == 2
    assert sched[0]["drawdown"] == 500000
    # Interest first period: 500k *1% =5000 capitalized
    assert sched[0]["interest_accrued"] == pytest.approx(5000)
    assert sched[0]["balance"] == pytest.approx(505000)
    # Second period: balance 505k +500k =1005k; interest 10050
    assert sched[1]["interest_accrued"] == pytest.approx(10050)

def test_financing_schedule_cash_interest():
    sched = build_financing_schedule(
        total_debt=1000000,
        drawdown_schedule=[1000000],
        interest_rate_annual=0.12,
        capitalize_interest=False
    )
    assert sched[0]["interest_cash"] == pytest.approx(10000)
    assert sched[0]["interest_capitalized"] == 0
    assert sched[0]["balance"] == 1000000  # not capitalized

def test_dscr_series():
    ocf = [200000, 150000, 0]
    ds = [100000, 100000, 100000]
    dscr = calculate_dscr_series(ocf, ds)
    assert dscr[0] == 2.0
    assert dscr[1] == 1.5
    assert dscr[2] == 0.0
    # Zero debt service
    dscr2 = calculate_dscr_series([100000], [0])
    assert dscr2[0] is None or dscr2[0] == float('inf')

def test_interest_coverage():
    assert calculate_interest_coverage(200000, 50000) == 4.0
    assert calculate_interest_coverage(200000, 0) is None

def test_debt_yield():
    assert calculate_debt_yield(100000, 1000000) == 10.0
    assert calculate_debt_yield(100000, 0) is None

def test_facility_headroom():
    res = calculate_facility_headroom(1000000, 600000)
    assert res["headroom"] == 400000
    assert res["utilization_pct"] == 60.0
    assert res["is_breached"] == False
    res2 = calculate_facility_headroom(1000000, 1100000)
    assert res2["is_breached"] == True

def test_levered_vs_unlevered():
    ul = [ -1000000, 200000, 300000]
    dd = [ 500000, 500000, 0]
    ds = [ 0, 50000, 50000]
    res = levered_vs_unlevered(ul, dd, ds)
    assert res["levered"][0] == -500000  # -1000+500-0
    assert res["levered"][1] == 650000   # 200+500-50
    assert res["levered"][2] == 250000   # 300+0-50

def test_financing_pct_drawdown():
    # Test % style: 0.5 =50%
    sched = build_financing_schedule(
        total_debt=1000000,
        drawdown_schedule=[0.5, 0.5],
        interest_rate_annual=0.10
    )
    assert sched[0]["drawdown"] == 500000
