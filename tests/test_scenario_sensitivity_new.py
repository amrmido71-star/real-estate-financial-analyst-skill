import pytest
from skill.tools.scenario_analysis import run_scenarios, run_sensitivity_analysis, run_two_way_sensitivity, tornado_sensitivity

def base_case():
    return {
        "gdv": 500_000_000,
        "gdc": 350_000_000,
        "cash_flows": [-350_000_000, 150_000_000, 200_000_000, 250_000_000],
        "discount_rate": 0.12,
        "sellable_area": 10000,
        "price_per_sqm": 50000,
        "cost_breakdown": {"land": 70_000_000, "construction": 200_000_000, "soft": 30_000_000, "marketing": 20_000_000, "financing": 30_000_000},
        "units": [{"units": 100, "price_per_unit": 5_000_000}],
    }

def test_scenario_true_rebuild():
    base = base_case()
    best = {"selling_price_change_pct": 8, "construction_cost_change_pct": -7}
    worst = {"selling_price_change_pct": -10, "construction_cost_change_pct": 15}
    result = run_scenarios(base, best, worst)
    assert result["best"]["gdv"] > result["base"]["gdv"]
    assert result["worst"]["gdv"] < result["base"]["gdv"]
    assert result["best"]["gdc"] < result["base"]["gdc"]
    assert result["worst"]["gdc"] > result["base"]["gdc"]
    assert result["best"]["profit"] > result["base"]["profit"]
    assert result["worst"]["profit"] < result["base"]["profit"]
    # IRR should also reflect
    assert result["best"]["irr"] > result["base"]["irr"]
    assert result["worst"]["irr"] < result["base"]["irr"]
    # Peak funding should be recomputed (not just KPI)
    assert "peak_funding" in result["best"]

def test_sensitivity_rebuilds_cashflow():
    base = base_case()
    results = run_sensitivity_analysis(base, "selling_price", [-10, 0, 10])
    # -10% should have lower profit and IRR than +10%
    assert results[0]["profit"] < results[2]["profit"]
    assert results[0]["gdv"] < results[2]["gdv"]
    # Ensure cash flows were rebuilt (positive flows scaled)
    assert results[0]["cash_flows"][1] < results[2]["cash_flows"][1]

def test_sensitivity_construction():
    base = base_case()
    results = run_sensitivity_analysis(base, "construction_cost", [-10, 10])
    # Higher construction => lower profit
    assert results[0]["profit"] > results[1]["profit"]

def test_two_way_sensitivity():
    base = base_case()
    matrix = run_two_way_sensitivity(base, "selling_price", [-10, 0, 10], "construction_cost", [-10, 0, 10], metric="profit")
    assert len(matrix["matrix"]) == 3
    assert len(matrix["matrix"][0]) == 3
    # Best corner: price +10, cost -10 => highest profit
    assert matrix["matrix"][2][0] > matrix["matrix"][0][2]  # row price +10 col cost -10 vs price -10 cost +10

def test_tornado_ranking():
    base = base_case()
    tornado = tornado_sensitivity(base, ["selling_price", "construction_cost", "collection_rate"], change_pct=10, metric="profit")
    assert len(tornado) == 3
    # Spread should be positive for at least one
    assert any(t["spread"] is not None and t["spread"] > 0 for t in tornado)
    # Sorted descending
    spreads = [t["spread"] or 0 for t in tornado]
    assert spreads == sorted(spreads, reverse=True)

def test_scenario_legacy_compat():
    # Legacy multiplier style should still work
    base = {"gdv": 500_000_000, "gdc": 350_000_000, "cash_flows": [-350_000_000, 200000000,200000000], "discount_rate":0.12}
    result = run_scenarios(base, {"gdv":1.08, "gdc":0.93}, {"gdv":0.90, "gdc":1.15})
    assert result["best"]["gdv"] == pytest.approx(540_000_000, rel=1e-6)
    assert result["worst"]["gdc"] == pytest.approx(402_500_000, rel=1e-6)

def test_delay_sensitivity():
    base = base_case()
    results = run_sensitivity_analysis(base, "delay", [0, 6])
    # Delay should affect cash flows length and maybe IRR lower
    # For delay 6 months, cash flows should be longer
    assert len(results[1]["cash_flows"]) >= len(results[0]["cash_flows"])
