"""
data_validation.py — Data Quality Checks for Real Estate Financial Data
"""

from typing import List, Dict, Any, Optional


def validate_financials(data: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Validate financial statement data.
    data: dict with keys like revenue, cost_of_revenue, units etc.
    Returns: {"errors": [...], "warnings": [...], "info": [...]}
    """
    errors = []
    warnings = []
    info = []

    revenue = data.get("revenue")
    cor = data.get("cost_of_revenue")
    gross_profit = data.get("gross_profit")
    total_units = data.get("total_units")
    sold_units = data.get("sold_units")

    # Negative revenue
    if revenue is not None and revenue < 0:
        errors.append("Revenue is negative — check data entry or credit notes handling (should be positive).")

    # Negative cost without explanation
    if cor is not None and cor < 0:
        warnings.append("Cost of Revenue is negative — unusual, verify if it's a reversal or error.")

    # Gross profit mismatch
    if revenue is not None and cor is not None and gross_profit is not None:
        expected = revenue - cor
        if abs(expected - gross_profit) > 0.01:
            warnings.append(f"Gross Profit mismatch: reported {gross_profit:,.2f} vs calculated {expected:,.2f} (Revenue - COR).")

    # Negative units
    if total_units is not None and total_units < 0:
        errors.append("Total Units is negative — impossible.")
    if sold_units is not None and sold_units < 0:
        errors.append("Sold Units is negative — impossible.")

    # Sold > Total
    if total_units is not None and sold_units is not None and sold_units > total_units:
        errors.append(f"Sold Units ({sold_units}) exceeds Total Units ({total_units}) — data error.")

    # Missing critical
    if revenue is None:
        info.append("Revenue is missing — cannot calculate Gross Margin, Net Margin.")
    if cor is None:
        info.append("Cost of Revenue is missing — cannot calculate Gross Profit accurately.")

    # Negative area
    sellable = data.get("sellable_area")
    bua = data.get("built_up_area")
    if sellable is not None and sellable < 0:
        errors.append("Sellable Area is negative — impossible.")
    if bua is not None and bua < 0:
        errors.append("Built-Up Area is negative — impossible.")
    if sellable is not None and bua is not None and sellable > bua:
        warnings.append(f"Sellable Area ({sellable:,.0f}) exceeds Built-Up Area ({bua:,.0f}) — check: sellable should be <= BUA.")

    # Date checks (if provided)
    sale_date = data.get("sale_date")
    collection_date = data.get("collection_date")
    # Simple string check placeholder — if both present and collection < sale, flag
    if sale_date and collection_date and str(collection_date) < str(sale_date):
        warnings.append("Collection Date is before Sale Date — check date logic.")

    return {"errors": errors, "warnings": warnings, "info": info}


def validate_project(project: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate project-level data"""
    errors = []
    warnings = []
    info = []

    gdv = project.get("gdv")
    gdc = project.get("gdc")
    land = project.get("land_cost")
    construction = project.get("construction_cost")
    sellable = project.get("sellable_area")
    bua = project.get("built_up_area")

    if gdv is not None and gdv < 0:
        errors.append("GDV is negative — impossible.")
    if gdc is not None and gdc < 0:
        errors.append("GDC is negative — impossible.")
    if land is not None and land < 0:
        errors.append("Land Cost is negative — check.")
    if construction is not None and construction < 0:
        errors.append("Construction Cost is negative — check.")

    if gdv is not None and gdc is not None and gdc > gdv:
        warnings.append(f"GDC ({gdc:,.0f}) exceeds GDV ({gdv:,.0f}) — project is loss-making at current assumptions (negative margin).")

    # Cost ratios
    if gdc and land:
        land_pct = land / gdc * 100
        if land_pct > 35:
            warnings.append(f"Land Cost {land_pct:.1f}% of GDC exceeds typical 15-30% — land may be overpriced or density low.")
    if gdc and construction:
        const_pct = construction / gdc * 100
        if const_pct > 70:
            warnings.append(f"Construction {const_pct:.1f}% of GDC exceeds typical 40-65% — check scope or cost overrun.")

    # GDV vs GDC sum checks if unit mix provided
    unit_mix = project.get("unit_mix")
    if unit_mix and gdv is not None:
        calc_gdv = sum(u.get("units", 0) * u.get("price_per_unit", 0) for u in unit_mix)
        if abs(calc_gdv - gdv) > 1.0:
            warnings.append(f"GDV mismatch: reported {gdv:,.0f} vs sum(unit_mix) {calc_gdv:,.0f}.")

    cost_breakdown = project.get("cost_breakdown")
    if cost_breakdown and gdc is not None:
        calc_gdc = sum(v for v in cost_breakdown.values() if v is not None)
        if abs(calc_gdc - gdc) > 1.0:
            warnings.append(f"GDC mismatch: reported {gdc:,.0f} vs sum(cost_breakdown) {calc_gdc:,.0f}.")

    if sellable is not None and sellable == 0:
        errors.append("Sellable Area is zero — cannot calculate Price/SQM or Profit/SQM.")
    if not project.get("unit_mix") and not gdv:
        info.append("No unit mix and no GDV provided — cannot assess revenue.")

    return {"errors": errors, "warnings": warnings, "info": info}


def validate_cashflow(cashflow_data: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate cash flow data"""
    errors = []
    warnings = []
    info = []

    inflows = cashflow_data.get("inflows", [])
    outflows = cashflow_data.get("outflows", [])
    cumulative = cashflow_data.get("cumulative")
    opening = cashflow_data.get("opening_cash", 0)

    if inflows and any(v is not None and v < 0 for v in inflows):
        warnings.append("Inflows contain negative values — verify sign convention (inflows should be positive).")
    if outflows and any(v is not None and v < 0 for v in outflows):
        warnings.append("Outflows contain negative values — outflows should be positive numbers (subtracted).")

    # Cumulative check
    if cumulative and inflows and outflows:
        # Recompute expected cumulative
        n = min(len(inflows), len(outflows), len(cumulative))
        running = opening
        for i in range(n):
            running += (inflows[i] or 0) - (outflows[i] or 0)
            if abs(running - cumulative[i]) > 1.0:
                errors.append(f"Cumulative mismatch at period {i+1}: reported {cumulative[i]:,.0f} vs calculated {running:,.0f}.")
                break

    # Collection > Contracted
    contracted = cashflow_data.get("contracted_sales")
    collected = cashflow_data.get("collected_cash")
    if contracted is not None and collected is not None and collected > contracted:
        errors.append(f"Collected Cash ({collected:,.0f}) exceeds Contracted Sales ({contracted:,.0f}) — check.")

    # Budget mismatch
    budget_total = cashflow_data.get("budget_total")
    budget_months = cashflow_data.get("budget_months")
    if budget_total is not None and budget_months:
        calc = sum(budget_months)
        if abs(calc - budget_total) > 1.0:
            warnings.append(f"Budget total mismatch: reported {budget_total:,.0f} vs sum(months) {calc:,.0f}.")

    if not inflows and not outflows:
        info.append("No cash flow data provided — cannot analyze liquidity.")

    return {"errors": errors, "warnings": warnings, "info": info}


def validate_sales_report(units: List[Dict]) -> Dict[str, List[str]]:
    """Validate sales/inventory data"""
    errors = []
    warnings = []
    info = []

    seen_codes = set()
    for idx, u in enumerate(units):
        code = u.get("unit_code", u.get("code", f"row_{idx}"))
        if code in seen_codes:
            errors.append(f"Duplicate unit code: {code} at row {idx+1}.")
        seen_codes.add(code)

        price = u.get("price_per_unit", u.get("price"))
        area = u.get("area")
        if price is not None and price < 0:
            errors.append(f"Negative price for unit {code}.")
        if area is not None and area < 0:
            errors.append(f"Negative area for unit {code}.")
        if area is not None and area == 0:
            warnings.append(f"Zero area for unit {code} — check.")

    return {"errors": errors, "warnings": warnings, "info": info}
