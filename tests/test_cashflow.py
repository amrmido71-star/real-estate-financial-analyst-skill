import pytest
from skill.tools.cashflow_analysis import (
    calculate_cumulative_cashflow,
    calculate_peak_funding,
    calculate_net_cashflow,
    calculate_free_cashflow,
    calculate_dscr,
    calculate_runway,
    calculate_collection_metrics,
    analyze_cashflow,
)


def test_cumulative():
    assert calculate_cumulative_cashflow([10, -5, 20], opening_cash=0) == [10, 5, 25]
    assert calculate_cumulative_cashflow([10, -5, 20], opening_cash=5) == [15, 10, 30]
    assert calculate_cumulative_cashflow([], opening_cash=10) == []


def test_peak_funding():
    # Cumulative: 10, 5, 25, -10 (peak is -10)
    cum = [10, 5, 25, -10, 15]
    peak = calculate_peak_funding(cum)
    assert peak["peak_amount"] == 10
    assert peak["peak_period"] == 3
    assert peak["peak_cumulative"] == -10

    # Never negative -> 0
    peak2 = calculate_peak_funding([10, 20, 30])
    assert peak2["peak_amount"] == 0

    # Empty
    assert calculate_peak_funding([]) is None


def test_net_cashflow():
    inflows = [100, 200, 150]
    outflows = [50, 100, 80]
    financing = [0, 0, 0]
    assert calculate_net_cashflow(inflows, outflows, financing) == [50, 100, 70]

    # With financing draw
    financing2 = [50, 0, 0]
    assert calculate_net_cashflow(inflows, outflows, financing2) == [100, 100, 70]

    # No financing
    assert calculate_net_cashflow([100], [50]) == [50]

    # Different lengths padded
    assert calculate_net_cashflow([100, 200], [50]) == [50, 200]


def test_free_cashflow():
    assert calculate_free_cashflow([50, 60], [-30, -40]) == [20, 20]
    assert calculate_free_cashflow([50], [-30, -40]) == [20, -40]


def test_dscr():
    assert calculate_dscr(150, 100) == 1.5
    assert calculate_dscr(80, 100) == 0.8
    assert calculate_dscr(150, 0) is None
    assert calculate_dscr(None, 100) is None


def test_runway():
    assert calculate_runway(100, 25) == 4.0
    assert calculate_runway(100, 0) is None
    assert calculate_runway(None, 25) is None


def test_collection_metrics():
    m = calculate_collection_metrics(100, 85, 100)
    assert m["outstanding_receivables"] == 15
    assert m["collection_efficiency_pct"] == 85.0

    m2 = calculate_collection_metrics(100, 85, 0)
    assert m2["collection_efficiency_pct"] is None


def test_analyze_cashflow():
    inflows = [10, 20, 30]
    outflows = [15, 10, 10]
    result = analyze_cashflow(inflows, outflows, opening_cash=5)
    assert result["periods"] == 3
    assert result["net_cashflow"] == [-5, 10, 20]
    assert result["cumulative_cashflow"] == [0, 10, 30]
    assert result["opening_cash"] == 5
    assert result["closing_cash"] == 30
    assert result["peak_funding"]["peak_amount"] == 0  # never negative

    # With trough
    result2 = analyze_cashflow([10, 10], [50, 5], opening_cash=0)
    assert result2["cumulative_cashflow"] == [-40, -35]
    assert result2["peak_funding"]["peak_amount"] == 40


def test_example_cashflow():
    # First 5 months of example_cashflow.csv (simplified)
    inflows = [58_000_000, 12_000_000, 45_000_000, 18_000_000, 22_000_000]
    outflows = [34_500_000, 36_500_000, 44_300_000, 49_800_000, 46_800_000]
    # Net: 23.5, -24.5, 0.7, -31.8, -24.8 (from CSV)
    net = calculate_net_cashflow(inflows, outflows)
    assert net[0] == 23_500_000
    assert net[1] == -24_500_000
    assert net[3] == -31_800_000

    cum = calculate_cumulative_cashflow(net, opening_cash=0)
    assert cum[0] == 23_500_000
    assert cum[1] == -1_000_000
    assert cum[3] == -32_100_000  # cumulative after 4 periods

    peak = calculate_peak_funding(cum)
    assert peak["peak_period"] == 4  # cumulative min at index 4 (-56.9M)
    assert peak["peak_amount"] == pytest.approx(56_900_000, rel=1e-3)
