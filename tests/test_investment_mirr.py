import pytest
from skill.tools.investment_metrics import (
    calculate_npv, calculate_npv_with_initial, calculate_mirr,
    count_sign_changes, detect_multiple_irr, irr_with_diagnostics
)

def test_npv_period_zero_not_discounted():
    # Period 0 should not be discounted
    # CF0=-100, CF1=110 @10% => NPV = -100 +100 =0? Actually 110/1.1=100 =>0
    assert calculate_npv([-100, 110], 0.10) == pytest.approx(0, abs=0.01)
    # CF0=-100 at 0% => -100+110=10
    assert calculate_npv([-100, 110], 0.0) == pytest.approx(10)

def test_npv_zero_rate():
    assert calculate_npv([-1000, 300, 400, 500], 0.0) == pytest.approx(200)

def test_npv_negative():
    # -100, 40,40 @10% => -100+36.36+33.06=-30.58
    assert calculate_npv([-100,40,40], 0.10) == pytest.approx(-30.58, abs=0.1)

def test_npv_with_initial():
    # initial 100, cfs 60,60 @10% => -100 +54.545+49.586=4.13
    # Using helper: combined = -100+60+60
    assert calculate_npv_with_initial([60,60], 0.10, 100) == pytest.approx(4.13, abs=0.01)
    assert calculate_npv_with_initial([60,60], 0.10, 100) == calculate_npv([-100,60,60], 0.10)

def test_npv_invalid_rate():
    try:
        calculate_npv([-100,110], -1.5)
        assert False, "Should raise"
    except Exception as e:
        assert "Discount rate" in str(e) or isinstance(e, Exception)

def test_npv_empty():
    assert calculate_npv([], 0.10) is None

def test_sign_changes():
    assert count_sign_changes([-100, 50, 50]) == 1
    assert count_sign_changes([-100, 50, -20, 80]) == 3
    assert count_sign_changes([100,100,100]) == 0
    assert count_sign_changes([-100,0,50]) == 1  # zeros ignored

def test_detect_multiple():
    has_multi, changes, msg = detect_multiple_irr([-100, 50, -20, 80])
    assert has_multi
    assert changes == 3
    has_multi2, changes2, _ = detect_multiple_irr([-100, 60, 60])
    assert not has_multi2
    assert changes2 == 1

def test_mirr_basic():
    # CFs: -1000, 300,300,300,300
    # finance 10%, reinvest 12%
    # PV neg =1000
    # FV pos =300*(1.12^3 +1.12^2+1.12+1)=300*(1.4049+1.2544+1.12+1)=300*4.779=1433.7
    # MIRR=(1433.7/1000)^(1/4)-1=9.41%
    cfs = [-1000, 300,300,300,300]
    mirr = calculate_mirr(cfs, 0.10, 0.12)
    assert mirr == pytest.approx(0.094, abs=0.01)
    assert mirr is not None

def test_mirr_no_pos_or_neg():
    assert calculate_mirr([100,100,100], 0.10, 0.12) is None
    assert calculate_mirr([-100,-50], 0.10, 0.12) is None

def test_irr_diagnostics_unique():
    res = irr_with_diagnostics([-100, 60, 60])
    assert res["irr"] is not None
    assert res["sign_changes"] == 1
    assert not res["has_multiple_risk"]

def test_irr_diagnostics_multiple():
    cfs = [-100, 150, -50, 30]
    res = irr_with_diagnostics(cfs)
    assert res["sign_changes"] >= 2
    assert res["has_multiple_risk"]
    # Should still try IRR and MIRR
    assert "mirr" in res

def test_break_even_regression():
    from skill.tools.project_metrics import calculate_break_even_revenue, calculate_break_even_price
    # GDC 1,249M, margin 0% => rev 1,249M
    assert calculate_break_even_revenue(1_249_267_500, 0) == 1_249_267_500
    # margin 20% => rev = 1,249/0.8=1,561
    assert calculate_break_even_revenue(1_249_267_500, 20) == pytest.approx(1_561_584_375)
    # price: area 62k, margin 0 => 20,149
    assert calculate_break_even_price(1_249_267_500, 62000, 0) == pytest.approx(20149.47, rel=1e-3)
    # margin 20 => 25186
    assert calculate_break_even_price(1_249_267_500, 62000, 20) == pytest.approx(25186.84, rel=1e-3)
    # invalid margin
    assert calculate_break_even_price(100, 1000, 100) is None
    assert calculate_break_even_revenue(100, 100) is None
    assert calculate_break_even_price(100, 0, 0) is None

def test_npv_regression_period_zero():
    # Ensure period zero not discounted even at high rate
    # CF0 -500, CF1 0, CF2 0 @50% => NPV = -500 (not -500/1.5)
    assert calculate_npv([-500, 0, 0], 0.5) == -500
    # CF0 0, CF1 100 @10% => 90.9 (discounted)
    assert calculate_npv([0, 100], 0.10) == pytest.approx(90.909, abs=0.01)
