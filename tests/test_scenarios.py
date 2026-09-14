import pytest
from skill.tools.scenario_analysis import run_scenarios, run_sensitivity_analysis, tornado_sensitivity


def test_run_scenarios_simple():
    base = {"gdv": 500_000_000, "gdc": 350_000_000, "discount_rate": 0.15, "cash_flows": [-350_000_000, 100_000_000, 150_000_000, 200_000_000]}
    best = {"gdv": 1.08, "gdc": 0.93}  # +8% GDV, -7% cost
    worst = {"gdv": 0.90, "gdc": 1.15}

    result = run_scenarios(base, best, worst)
    assert "best" in result and "base" in result and "worst" in result
    # Best should have higher profit than base, worst lower
    assert result["best"]["profit"] > result["base"]["profit"]
    assert result["worst"]["profit"] < result["base"]["profit"]
    assert result["best"]["margin_pct"] > result["base"]["margin_pct"]
    assert result["worst"]["margin_pct"] < result["base"]["margin_pct"]


def test_run_scenarios_with_custom_calc():
    def calc(scenario):
        # Simple: profit = gdv - gdc, return dict
        return {"profit": scenario["gdv"] - scenario["gdc"], "gdv": scenario["gdv"]}

    base = {"gdv": 100, "gdc": 60}
    result = run_scenarios(base, {"gdv": 1.10}, {"gdv": 0.90}, calc_fn=calc)
    assert result["best"]["profit"] == pytest.approx(50)  # 110-60
    assert result["base"]["profit"] == pytest.approx(40)
    assert result["worst"]["profit"] == pytest.approx(30)


def test_sensitivity():
    base = {"gdv": 500_000_000, "gdc": 350_000_000, "discount_rate": 0.10, "cash_flows": [-350_000_000, 200_000_000, 200_000_000, 200_000_000]}
    # Test gdv sensitivity +-10%
    results = run_sensitivity_analysis(base, "gdv", [-10, 0, 10])
    assert len(results) == 3
    # -10% gdv should give lower profit than +10%
    assert results[0]["profit"] < results[2]["profit"]
    assert results[1]["profit"] == pytest.approx(150_000_000)

    # Price sensitivity via gdv
    results_price = run_sensitivity_analysis(base, "price", [-10, 10])
    # Uses generic fallback that scales gdv
    assert len(results_price) == 2


def test_sensitivity_gdc():
    base = {"gdv": 500_000_000, "gdc": 350_000_000, "discount_rate": 0.10, "cash_flows": [-350_000_000, 200_000_000, 200_000_000]}
    results = run_sensitivity_analysis(base, "gdc", [-10, 0, 10])
    # Higher gdc => lower profit
    assert results[0]["profit"] > results[2]["profit"]


def test_tornado():
    base = {"gdv": 500_000_000, "gdc": 350_000_000, "discount_rate": 0.12, "cash_flows": [-350_000_000, 150_000_000, 200_000_000, 250_000_000]}
    tornado = tornado_sensitivity(base, ["gdv", "gdc"], change_pct=10, metric="profit")
    assert len(tornado) == 2
    # Sorted by spread descending
    assert tornado[0]["spread"] >= tornado[1]["spread"]
    # Check structure
    assert "variable" in tornado[0]
    assert "down" in tornado[0]
    assert "up" in tornado[0]


def test_scenario_format():
    from skill.tools.scenario_analysis import format_scenario_table
    scenarios = {
        "best": {"gdv": 540_000_000, "gdc": 325_000_000, "profit": 215_000_000},
        "base": {"gdv": 500_000_000, "gdc": 350_000_000, "profit": 150_000_000},
        "worst": {"gdv": 450_000_000, "gdc": 402_000_000, "profit": 48_000_000},
    }
    table = format_scenario_table(scenarios, metrics=["gdv", "gdc", "profit"])
    assert "| Metric | Best | Base | Worst |" in table
    assert "gdv" in table


def test_green_valley_scenarios():
    # Replicate Green Valley scenario logic
    base = {"gdv": 1_750_500_000, "gdc": 1_249_267_500, "discount_rate": 0.15, "cash_flows": [-420_000_000, -380_000_000, 150_000_000, 680_000_000, 471_232_500]}
    best_adj = {"gdv": 1.08, "gdc": 0.93}
    worst_adj = {"gdv": 0.90, "gdc": 1.15}
    result = run_scenarios(base, best_adj, worst_adj)
    # Base profit ~501M
    assert result["base"]["profit"] == pytest.approx(501_232_500, rel=1e-4)
    # Best profit > base
    assert result["best"]["profit"] > 700_000_000
    # Worst profit ~139M (per example)
    assert result["worst"]["profit"] == pytest.approx(139_000_000, abs=10_000_000)
