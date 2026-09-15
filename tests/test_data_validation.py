from datetime import date
from skill.tools.data_validation import (
    validate_financials, validate_project, validate_cashflow,
    validate_sales_report, validate_transactions,
    calculate_data_quality_score, assess_confidence,
    _parse_date
)

def test_parse_date_valid():
    assert _parse_date("2025-01-15") == date(2025,1,15)
    assert _parse_date("15/01/2025") == date(2025,1,15)
    assert _parse_date(date(2025,1,15)) == date(2025,1,15)
    assert _parse_date("2025/01/15") == date(2025,1,15)

def test_parse_date_invalid():
    assert _parse_date("invalid") is None
    assert _parse_date("") is None
    assert _parse_date(None) is None

def test_validate_financials_negative_revenue():
    result = validate_financials({"revenue": -100})
    assert any("negative" in e.lower() for e in result["errors"])

def test_validate_financials_sold_exceeds_total():
    result = validate_financials({"total_units": 100, "sold_units": 120})
    assert len(result["errors"]) > 0

def test_validate_financials_sellable_gt_bua():
    result = validate_financials({"sellable_area": 10000, "built_up_area": 8000})
    assert len(result["warnings"]) > 0

def test_validate_financials_date_logic():
    result = validate_financials({"sale_date": "2025-06-01", "collection_date": "2025-05-01"})
    assert len(result["errors"]) > 0

def test_validate_financials_future_sale():
    result = validate_financials({"sale_date": "2099-01-01"})
    assert any("future" in w.lower() for w in result["warnings"])

def test_validate_project_gdc_exceeds_gdv():
    result = validate_project({"gdv": 100, "gdc": 150})
    assert len(result["warnings"]) > 0

def test_validate_project_land_pct():
    result = validate_project({"gdc": 100, "land_cost": 40})
    assert any("land" in w.lower() for w in result["warnings"])

def test_validate_project_date_sequence():
    result = validate_project({"start_date": "2026-01-01", "delivery_date": "2025-01-01"})
    assert len(result["errors"]) > 0

def test_validate_project_gdv_mismatch():
    result = validate_project({"gdv": 1000000, "unit_mix": [{"units":10, "price_per_unit":50000}]})
    assert len(result["warnings"]) > 0

def test_validate_cashflow_negative_inflows():
    result = validate_cashflow({"inflows": [-10, 20], "outflows": [5,5]})
    assert len(result["warnings"]) > 0

def test_validate_cashflow_cumulative_mismatch():
    result = validate_cashflow({"inflows": [100,100], "outflows": [20,20], "cumulative": [80, 200], "opening_cash":0})
    assert len(result["errors"]) > 0

def test_validate_cashflow_collected_exceeds_contracted():
    result = validate_cashflow({"contracted_sales": 100, "collected_cash": 150})
    assert len(result["errors"]) > 0

def test_validate_sales_report_duplicate():
    units = [{"unit_code":"A1","price_per_unit":100000,"area":100},{"unit_code":"A1","price_per_unit":100000,"area":100}]
    result = validate_sales_report(units)
    assert len(result["errors"]) > 0

def test_validate_sales_report_negative():
    units = [{"unit_code":"A1","price_per_unit":-100000,"area":100}]
    result = validate_sales_report(units)
    assert len(result["errors"]) > 0

def test_validate_transactions_duplicate():
    txns = [{"transaction_id":"T1","amount":100,"date":"2025-01-01"},{"transaction_id":"T1","amount":200,"date":"2025-01-02"}]
    result = validate_transactions(txns)
    assert len(result["errors"]) > 0

def test_data_quality_score():
    vr = {"errors": ["e1","e2"], "warnings": ["w1"], "info": ["missing field: gdv"]}
    score = calculate_data_quality_score(vr)
    assert score["score"] < 100
    assert score["confidence"] == "Medium"  # 2 critical + 1 warning => Medium per scoring
    assert score["critical_errors"] == 2

def test_assess_confidence():
    assert assess_confidence(90, False, 0.2, 90) == "High"
    assert assess_confidence(40, True, 0.9, 40) == "Low"
    assert assess_confidence(60, True, 0.5) == "Medium"

def test_zero_sellable_area():
    result = validate_financials({"sellable_area": 0})
    assert len(result["errors"]) > 0

def test_currency_validation():
    result = validate_financials({"currency": "XYZ"})
    assert len(result["warnings"]) > 0
