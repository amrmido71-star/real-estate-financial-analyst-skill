"""
data_validation.py — Data Quality Checks for Real Estate Financial Data
Enhanced with datetime parsing, type validation, business rules, quality scoring
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
import re


def _parse_date(value: Any) -> Optional[date]:
    """Parse various date formats into date object; returns None if invalid"""
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    s = str(value).strip()
    if not s:
        return None
    # Try common formats
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y", "%Y.%m.%d", "%d.%m.%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt).date()
        except:
            continue
    # Try ISO with time
    try:
        return datetime.fromisoformat(s).date()
    except:
        return None


def _is_numeric(value: Any) -> bool:
    if value is None:
        return False
    try:
        float(str(value).replace(",", "").replace("EGP","").replace("SAR","").strip())
        return True
    except:
        return False


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace(",", "").replace("EGP","").replace("SAR","").replace("$","").replace("%","").strip()
    if s == "" or s == "-":
        return None
    try:
        return float(s)
    except:
        return None


def validate_financials(data: Dict[str, Any]) -> Dict[str, List[str]]:
    errors = []
    warnings = []
    info = []

    revenue = _to_float(data.get("revenue"))
    cor = _to_float(data.get("cost_of_revenue", data.get("cogs")))
    gross_profit = _to_float(data.get("gross_profit"))
    total_units = _to_float(data.get("total_units"))
    sold_units = _to_float(data.get("sold_units"))

    # Type validation
    for field in ["revenue", "cost_of_revenue", "gross_profit"]:
        raw = data.get(field)
        if raw is not None and not _is_numeric(raw):
            errors.append(f"{field} is not numeric: '{raw}'")

    if revenue is not None and revenue < 0:
        errors.append("Revenue is negative — check data entry or credit notes handling (should be positive).")
    if cor is not None and cor < 0:
        warnings.append("Cost of Revenue is negative — unusual, verify if it's a reversal or error.")
    if revenue is not None and cor is not None and gross_profit is not None:
        expected = revenue - cor
        if abs(expected - gross_profit) > 0.01:
            warnings.append(f"Gross Profit mismatch: reported {gross_profit:,.2f} vs calculated {expected:,.2f} (Revenue - COR).")
    if total_units is not None and total_units < 0:
        errors.append("Total Units is negative — impossible.")
    if sold_units is not None and sold_units < 0:
        errors.append("Sold Units is negative — impossible.")
    if total_units is not None and sold_units is not None and sold_units > total_units:
        errors.append(f"Sold Units ({sold_units:.0f}) exceeds Total Units ({total_units:.0f}) — data error.")
    if revenue is None:
        info.append("Revenue is missing — cannot calculate Gross Margin, Net Margin.")
    if cor is None:
        info.append("Cost of Revenue is missing — cannot calculate Gross Profit accurately.")

    sellable = _to_float(data.get("sellable_area"))
    bua = _to_float(data.get("built_up_area"))
    if sellable is not None and sellable < 0:
        errors.append("Sellable Area is negative — impossible.")
    if bua is not None and bua < 0:
        errors.append("Built-Up Area is negative — impossible.")
    if sellable is not None and bua is not None and sellable > bua:
        warnings.append(f"Sellable Area ({sellable:,.0f}) exceeds Built-Up Area ({bua:,.0f}) — check: sellable should be <= BUA.")
    if sellable is not None and sellable == 0:
        errors.append("Sellable Area is zero — cannot calculate Price/SQM.")

    # Date validation with proper parsing
    sale_date_raw = data.get("sale_date")
    collection_date_raw = data.get("collection_date")
    sale_date = _parse_date(sale_date_raw)
    collection_date = _parse_date(collection_date_raw)
    if sale_date_raw and sale_date is None:
        errors.append(f"Invalid sale_date format: '{sale_date_raw}' — expected YYYY-MM-DD")
    if collection_date_raw and collection_date is None:
        errors.append(f"Invalid collection_date format: '{collection_date_raw}' — expected YYYY-MM-DD")
    if sale_date and collection_date and collection_date < sale_date:
        errors.append(f"Collection Date {collection_date} is before Sale Date {sale_date} — check date logic.")
    if sale_date and sale_date > date.today():
        warnings.append(f"Sale Date {sale_date} is in the future — check if forecast vs actual.")

    # Percentage validation
    for pct_field in ["gross_margin", "net_margin", "collection_efficiency"]:
        val = _to_float(data.get(pct_field))
        if val is not None and (val < -100 or val > 1000):
            warnings.append(f"{pct_field} {val}% seems unrealistic — check.")

    # Currency validation
    currency = data.get("currency")
    if currency and currency not in ["EGP","SAR","AED","USD","EUR","GBP"]:
        warnings.append(f"Currency '{currency}' not in supported list — check.")

    return {"errors": errors, "warnings": warnings, "info": info}


def validate_project(project: Dict[str, Any]) -> Dict[str, List[str]]:
    errors = []
    warnings = []
    info = []
    gdv = _to_float(project.get("gdv"))
    gdc = _to_float(project.get("gdc"))
    land = _to_float(project.get("land_cost"))
    construction = _to_float(project.get("construction_cost"))
    sellable = _to_float(project.get("sellable_area"))
    bua = _to_float(project.get("built_up_area"))

    if gdv is not None and gdv < 0:
        errors.append("GDV is negative — impossible.")
    if gdc is not None and gdc < 0:
        errors.append("GDC is negative — impossible.")
    if land is not None and land < 0:
        errors.append("Land Cost is negative — check.")
    if construction is not None and construction < 0:
        errors.append("Construction Cost is negative — check.")
    if gdv is not None and gdc is not None and gdc > gdv:
        warnings.append(f"GDC ({gdc:,.0f}) exceeds GDV ({gdv:,.0f}) — project is loss-making (negative margin).")
    if gdc and land:
        land_pct = land / gdc * 100
        if land_pct > 35:
            warnings.append(f"Land Cost {land_pct:.1f}% of GDC exceeds typical 15-30% — land may be overpriced.")
        if land_pct < 5:
            warnings.append(f"Land Cost {land_pct:.1f}% of GDC very low — check if land cost missing.")
    if gdc and construction:
        const_pct = construction / gdc * 100
        if const_pct > 70:
            warnings.append(f"Construction {const_pct:.1f}% of GDC exceeds typical 40-65% — check scope.")
        if const_pct < 20:
            warnings.append(f"Construction {const_pct:.1f}% very low — check if cost missing.")
    unit_mix = project.get("unit_mix")
    if unit_mix and gdv is not None:
        try:
            calc_gdv = sum((u.get("units",0) or 0) * (u.get("price_per_unit",0) or 0) for u in unit_mix)
            if abs(calc_gdv - gdv) > 1.0:
                warnings.append(f"GDV mismatch: reported {gdv:,.0f} vs sum(unit_mix) {calc_gdv:,.0f}.")
        except Exception as e:
            warnings.append(f"Could not reconcile unit_mix GDV: {e}")
    cost_breakdown = project.get("cost_breakdown")
    if cost_breakdown and gdc is not None:
        try:
            calc_gdc = sum(v for v in cost_breakdown.values() if v is not None and _is_numeric(v))
            calc_gdc = float(calc_gdc)
            if abs(calc_gdc - gdc) > 1.0:
                warnings.append(f"GDC mismatch: reported {gdc:,.0f} vs sum(cost_breakdown) {calc_gdc:,.0f}.")
        except Exception as e:
            warnings.append(f"Could not reconcile cost_breakdown: {e}")
    if sellable is not None and sellable == 0:
        errors.append("Sellable Area is zero — cannot calculate Price/SQM.")
    if sellable is not None and bua is not None and sellable > bua:
        warnings.append(f"Sellable {sellable:,.0f} > BUA {bua:,.0f} — check area logic.")
    # Date sequence
    start = _parse_date(project.get("start_date"))
    delivery = _parse_date(project.get("delivery_date"))
    if start and delivery and delivery < start:
        errors.append(f"Delivery Date {delivery} before Start Date {start} — impossible.")
    if not project.get("unit_mix") and not gdv:
        info.append("No unit mix and no GDV provided — cannot assess revenue.")
    # Required fields
    for req in ["gdv", "gdc", "sellable_area"]:
        if project.get(req) is None:
            info.append(f"Missing recommended field: {req}")
    return {"errors": errors, "warnings": warnings, "info": info}


def validate_cashflow(cashflow_data: Dict[str, Any]) -> Dict[str, List[str]]:
    errors = []
    warnings = []
    info = []
    inflows = cashflow_data.get("inflows", [])
    outflows = cashflow_data.get("outflows", [])
    cumulative = cashflow_data.get("cumulative")
    opening = _to_float(cashflow_data.get("opening_cash", 0)) or 0

    # Type checks
    for name, arr in [("inflows", inflows), ("outflows", outflows)]:
        for i, v in enumerate(arr):
            if v is not None and not _is_numeric(v):
                errors.append(f"{name}[{i}] not numeric: '{v}'")

    if inflows and any(_to_float(v) is not None and _to_float(v) < 0 for v in inflows if v is not None):
        warnings.append("Inflows contain negative values — inflows should be positive.")
    if outflows and any(_to_float(v) is not None and _to_float(v) < 0 for v in outflows if v is not None):
        warnings.append("Outflows contain negative values — outflows should be positive numbers.")
    if cumulative and inflows and outflows:
        n = min(len(inflows), len(outflows), len(cumulative))
        running = opening
        for i in range(n):
            iv = _to_float(inflows[i]) or 0
            ov = _to_float(outflows[i]) or 0
            running += iv - ov
            cv = _to_float(cumulative[i])
            if cv is not None and abs(running - cv) > 1.0:
                errors.append(f"Cumulative mismatch at period {i+1}: reported {cv:,.0f} vs calculated {running:,.0f}.")
                break
    contracted = _to_float(cashflow_data.get("contracted_sales"))
    collected = _to_float(cashflow_data.get("collected_cash"))
    if contracted is not None and collected is not None and collected > contracted:
        errors.append(f"Collected Cash ({collected:,.0f}) exceeds Contracted Sales ({contracted:,.0f}) — check.")
    # Due vs collected logic
    due = _to_float(cashflow_data.get("due_amount"))
    if due is not None and collected is not None and collected > due:
        warnings.append(f"Collected ({collected:,.0f}) > Due ({due:,.0f}) — check over-collection.")
    budget_total = _to_float(cashflow_data.get("budget_total"))
    budget_months = cashflow_data.get("budget_months")
    if budget_total is not None and budget_months:
        try:
            calc = sum(_to_float(v) or 0 for v in budget_months)
            if abs(calc - budget_total) > 1.0:
                warnings.append(f"Budget total mismatch: reported {budget_total:,.0f} vs sum(months) {calc:,.0f}.")
        except:
            pass
    if not inflows and not outflows:
        info.append("No cash flow data provided — cannot analyze liquidity.")
    # Date sequence for periods
    period_dates = cashflow_data.get("period_dates", [])
    if period_dates:
        parsed = [_parse_date(d) for d in period_dates]
        for i in range(1, len(parsed)):
            if parsed[i] and parsed[i-1] and parsed[i] < parsed[i-1]:
                errors.append(f"Period dates out of order: {period_dates[i-1]} -> {period_dates[i]}")
    return {"errors": errors, "warnings": warnings, "info": info}


def validate_sales_report(units: List[Dict]) -> Dict[str, List[str]]:
    errors = []
    warnings = []
    info = []
    seen_codes = set()
    for idx, u in enumerate(units):
        code = u.get("unit_code", u.get("code", f"row_{idx}"))
        if code in seen_codes:
            errors.append(f"Duplicate unit code: {code} at row {idx+1}.")
        seen_codes.add(code)
        price = _to_float(u.get("price_per_unit", u.get("price")))
        area = _to_float(u.get("area", u.get("area_sqm")))
        if price is not None and price < 0:
            errors.append(f"Negative price for unit {code}.")
        if price is not None and price == 0:
            warnings.append(f"Zero price for unit {code} — check.")
        if area is not None and area < 0:
            errors.append(f"Negative area for unit {code}.")
        if area is not None and area == 0:
            warnings.append(f"Zero area for unit {code} — check.")
        # Status validation
        status = u.get("status")
        if status and status not in ["available","reserved","sold","cancelled"]:
            warnings.append(f"Unknown status '{status}' for unit {code} — expected available/reserved/sold/cancelled.")
    if not units:
        info.append("No units provided — cannot assess inventory.")
    return {"errors": errors, "warnings": warnings, "info": info}


def validate_transactions(transactions: List[Dict]) -> Dict[str, List[str]]:
    """Check duplicate transaction IDs, missing fields"""
    errors = []
    warnings = []
    info = []
    seen = set()
    for idx, t in enumerate(transactions):
        tid = t.get("transaction_id", t.get("id", f"txn_{idx}"))
        if tid in seen:
            errors.append(f"Duplicate transaction ID: {tid} at row {idx+1}")
        seen.add(tid)
        if not t.get("amount") and t.get("amount") != 0:
            warnings.append(f"Missing amount for transaction {tid}")
        if not t.get("date"):
            warnings.append(f"Missing date for transaction {tid}")
        else:
            if _parse_date(t.get("date")) is None:
                errors.append(f"Invalid date '{t.get('date')}' for transaction {tid}")
    return {"errors": errors, "warnings": warnings, "info": info}


def calculate_data_quality_score(validation_result: Dict[str, List[str]], total_checks: int = 20, missing_fields: int = 0) -> Dict:
    """
    Data Quality Score 0-100
    Score = 100 - (critical*10 + warnings*3 + missing*5)  clamped 0-100
    Confidence derives from errors/warnings/missing
    """
    errors = len(validation_result.get("errors", []))
    warnings = len(validation_result.get("warnings", []))
    # info may contain missing
    infos = validation_result.get("info", [])
    # Count missing from info if mentions missing
    missing = missing_fields + sum(1 for i in infos if "missing" in i.lower())

    score = 100 - (errors * 15 + warnings * 4 + missing * 5)
    score = max(0, min(100, score))

    if errors >= 3 or score < 50:
        confidence = "Low"
    elif errors >= 1 or warnings >= 4 or score < 75:
        confidence = "Medium"
    else:
        confidence = "High"

    return {
        "score": int(score),
        "critical_errors": errors,
        "warnings": warnings,
        "missing_fields": missing,
        "confidence": confidence,
        "details": validation_result,
    }


def assess_confidence(
    data_completeness_pct: float,  # 0-100
    has_assumptions: bool,
    forecast_ratio: float,  # forecast / actual? >1 means more forecast
    quality_score: Optional[int] = None,
) -> str:
    """
    Confidence based on completeness, assumptions, forecast ratio
    """
    if data_completeness_pct < 50 or (quality_score is not None and quality_score < 50):
        return "Low"
    if data_completeness_pct < 75 or has_assumptions or forecast_ratio > 0.7:
        return "Medium"
    return "High"
