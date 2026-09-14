import pytest
from skill.tools.project_metrics import (
    calculate_gdv,
    calculate_gdv_from_area,
    calculate_gdc,
    calculate_development_profit,
    calculate_development_margin,
    calculate_margin_on_cost,
    calculate_cost_per_sqm,
    calculate_price_per_sqm,
    calculate_profit_per_sqm,
    calculate_land_cost_pct,
    calculate_construction_cost_pct,
    calculate_break_even_pct,
    calculate_break_even_price,
    calculate_residual_land_value,
    calculate_sales_rate,
    calculate_inventory_months,
    calculate_collection_efficiency,
)


def test_calculate_gdv():
    units = [
        {"units": 10, "price_per_unit": 1_000_000},
        {"units": 5, "price_per_unit": 2_000_000},
    ]
    assert calculate_gdv(units) == 20_000_000
    assert calculate_gdv([]) is None
    # Flexible keys
    units2 = [{"quantity": 10, "price": 500_000}]
    assert calculate_gdv(units2) == 5_000_000


def test_calculate_gdv_from_area():
    assert calculate_gdv_from_area(1000, 20000) == 20_000_000
    assert calculate_gdv_from_area(None, 20000) is None
    assert calculate_gdv_from_area(1000, None) is None


def test_calculate_gdc():
    breakdown = {"land": 50_000_000, "construction": 100_000_000, "soft": 10_000_000}
    assert calculate_gdc(breakdown) == 160_000_000
    assert calculate_gdc({}) is None
    assert calculate_gdc({"land": 50_000_000, "construction": None}) == 50_000_000


def test_development_profit_margin():
    assert calculate_development_profit(500_000_000, 350_000_000) == 150_000_000
    assert calculate_development_profit(None, 350_000_000) is None
    assert calculate_development_margin(500_000_000, 350_000_000) == 30.0
    assert calculate_development_margin(0, 350_000_000) is None
    assert calculate_development_margin(500_000_000, 500_000_000) == 0.0
    # Negative margin
    assert calculate_development_margin(300_000_000, 350_000_000) == pytest.approx(-16.666, rel=1e-2)


def test_margin_on_cost():
    assert calculate_margin_on_cost(500_000_000, 350_000_000) == pytest.approx(42.857, rel=1e-2)
    assert calculate_margin_on_cost(500_000_000, 0) is None


def test_per_sqm():
    assert calculate_cost_per_sqm(350_000_000, 10_000) == 35_000
    assert calculate_cost_per_sqm(350_000_000, 0) is None
    assert calculate_price_per_sqm(500_000_000, 10_000) == 50_000
    assert calculate_price_per_sqm(500_000_000, 0) is None
    assert calculate_profit_per_sqm(500_000_000, 350_000_000, 10_000) == 15_000
    assert calculate_profit_per_sqm(500_000_000, 350_000_000, 0) is None


def test_cost_ratios():
    assert calculate_land_cost_pct(50_000_000, 200_000_000) == 25.0
    assert calculate_land_cost_pct(50_000_000, 0) is None
    assert calculate_construction_cost_pct(120_000_000, 200_000_000) == 60.0


def test_break_even():
    assert calculate_break_even_pct(350_000_000, 500_000_000) == 70.0
    assert calculate_break_even_pct(500_000_000, 500_000_000) == 100.0
    assert calculate_break_even_pct(350_000_000, 0) is None
    # Break-even price with no target margin
    assert calculate_break_even_price(350_000_000, 10_000) == 35_000
    assert calculate_break_even_price(350_000_000, 0) is None
    # With target margin
    # GDC 350M, area 10k, target 20% => BE price = 350M / (0.8 * 10k) = 43,750
    assert calculate_break_even_price(350_000_000, 10_000, target_margin_pct=20) == pytest.approx(43_750)


def test_residual_land():
    # GDV 500M, costs 300M without land, profit 50M => land = 150M
    assert calculate_residual_land_value(500_000_000, construction=200_000_000, soft_costs=50_000_000, developer_profit=50_000_000) == 200_000_000
    assert calculate_residual_land_value(None, construction=100_000_000) is None


def test_sales_rate():
    assert calculate_sales_rate(250, 500) == 50.0
    assert calculate_sales_rate(250, 0) is None
    assert calculate_sales_rate(None, 500) is None


def test_inventory_months():
    assert calculate_inventory_months(100, 10) == 10.0
    assert calculate_inventory_months(100, 0) is None


def test_collection_efficiency():
    assert calculate_collection_efficiency(85, 100) == 85.0
    assert calculate_collection_efficiency(85, 0) is None


def test_green_valley_example():
    # From example_project.md mock data
    # Test GDC components
    cost_breakdown = {
        "land": 260_000_000,
        "construction": 620_000_000,
        "infrastructure": 65_000_000,
        "soft": 75_000_000,
        "sales_marketing": 61_267_500,
        "financing": 85_000_000,
        "admin": 30_000_000,
        "contingency": 31_000_000,
        "fees": 22_000_000,
    }
    gdc = calculate_gdc(cost_breakdown)
    assert gdc == 1_249_267_500

    gdv = 1_750_500_000
    margin = calculate_development_margin(gdv, gdc)
    assert margin == pytest.approx(28.64, rel=1e-2)

    # Per SQM
    sellable = 62_000
    bua = 82_000
    assert calculate_price_per_sqm(gdv, sellable) == pytest.approx(28_233.87, rel=1e-3)
    assert calculate_cost_per_sqm(gdc, bua) == pytest.approx(15_234.97, rel=1e-3)
    assert calculate_profit_per_sqm(gdv, gdc, sellable) == pytest.approx(8_084.68, rel=1e-3)

    # Break-even
    assert calculate_break_even_pct(gdc, gdv) == pytest.approx(71.37, rel=1e-2)
