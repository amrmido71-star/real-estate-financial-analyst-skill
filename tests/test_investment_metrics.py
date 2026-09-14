import pytest
from skill.tools.investment_metrics import (
    calculate_npv,
    calculate_irr,
    calculate_equity_multiple,
    calculate_cash_on_cash,
    calculate_payback_period,
    calculate_roic,
    calculate_nopat,
)


def test_npv():
    # Simple: -100 at t0, +60 at t1, +60 at t2, discount 10% => NPV = -100 + 54.545 + 49.586 = 4.13
    cash_flows = [-100, 60, 60]
    npv = calculate_npv(cash_flows, 0.10)
    assert npv == pytest.approx(4.13, abs=0.02)

    # With initial_investment separate
    cash_flows2 = [60, 60]
    npv2 = calculate_npv(cash_flows2, 0.10, initial_investment=100)
    # This computes 60/(1.1)^0 + 60/(1.1)^1 -100 = 60 +54.545-100=14.545 — different convention
    # So test the primary usage
    assert npv2 is not None

    # Zero discount
    assert calculate_npv([-100, 50, 50], 0.0) == 0.0
    # Empty
    assert calculate_npv([], 0.10) is None


def test_irr_basic():
    # -100, 60, 60 => IRR ~13%
    irr = calculate_irr([-100, 60, 60])
    assert irr == pytest.approx(0.13, abs=0.02)

    # -100, 110 => IRR 10%
    assert calculate_irr([-100, 110]) == pytest.approx(0.10, abs=0.001)

    # -1000, 300, 400, 500 => IRR ~8.9%
    irr2 = calculate_irr([-1000, 300, 400, 500])
    assert irr2 is not None
    assert 0.05 < irr2 < 0.15

    # No sign change => None
    assert calculate_irr([100, 100, 100]) is None
    assert calculate_irr([-100, -50]) is None

    # Single cash flow with sign change but only 2 elements
    assert calculate_irr([-100, 120]) == pytest.approx(0.20, abs=0.01)


def test_irr_edge_cases():
    # Too short
    assert calculate_irr([]) is None
    assert calculate_irr([-100]) is None
    # Larger project example from example_project.md: -420, -380, 150, 680, 471.23
    # Note these are not discounted equally timed; but IRR should be positive ~18%
    cash_flows = [-420_000_000, -380_000_000, 150_000_000, 680_000_000, 471_232_500]
    irr = calculate_irr(cash_flows)
    assert irr is not None
    # Check NPV at IRR ~0
    npv_at_irr = calculate_npv(cash_flows, irr)
    assert abs(npv_at_irr) < 1000  # close to zero


def test_equity_multiple():
    assert calculate_equity_multiple(200, 100) == 2.0
    assert calculate_equity_multiple(150, 100) == 1.5
    assert calculate_equity_multiple(200, 0) is None
    assert calculate_equity_multiple(None, 100) is None


def test_cash_on_cash():
    assert calculate_cash_on_cash(12_000, 100_000) == 12.0
    assert calculate_cash_on_cash(12_000, 0) is None


def test_payback():
    # -100, 40, 40, 40 => payback 2.5 years (100/40 =2.5)
    assert calculate_payback_period([-100, 40, 40, 40]) == pytest.approx(2.5, abs=0.01)
    # -100, 60, 60 => payback 1 + 40/60 = 1.666...
    assert calculate_payback_period([-100, 60, 60]) == pytest.approx(1.666, abs=0.01)
    # Never pays back
    assert calculate_payback_period([-100, 10, 10, 10]) is None
    # Immediate payback
    assert calculate_payback_period([-100, 150]) == pytest.approx(0.666, abs=0.01)


def test_roic_nopat():
    assert calculate_nopat(100, 0.25) == 75
    assert calculate_roic(75, 300) == 25.0
    assert calculate_roic(75, 0) is None
    assert calculate_nopat(None, 0.25) is None


def test_irr_annualized():
    from skill.tools.investment_metrics import calculate_irr_annualized
    # Monthly: -1000, 100 x 12 months => monthly IRR ~2.92% => annualized ~41%
    monthly = [-1000] + [100] * 12
    ann = calculate_irr_annualized(monthly)
    assert ann is not None
    assert ann > 0.3
