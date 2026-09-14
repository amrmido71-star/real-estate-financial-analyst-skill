"""
project_metrics.py — Real Estate Development Project Metrics
GDV, GDC, Margins, per-SQM, Cost Ratios, Break-even
"""

from typing import Optional, List, Dict


def calculate_gdv(units: List[Dict]) -> Optional[float]:
    """
    GDV = sum(units * price)
    units: list of dicts with keys: 'units' (int) and 'price_per_unit' OR 'quantity' and 'price'
    Flexible key handling.
    """
    if not units:
        return None
    total = 0.0
    for u in units:
        qty = u.get("units", u.get("quantity", u.get("count", 0)))
        price = u.get("price_per_unit", u.get("price", u.get("selling_price", 0)))
        total += qty * price
    return total


def calculate_gdv_from_area(sellable_area: Optional[float], price_per_sqm: Optional[float]) -> Optional[float]:
    """GDV = Sellable Area * Price per SQM"""
    if sellable_area is None or price_per_sqm is None:
        return None
    return sellable_area * price_per_sqm


def calculate_gdc(cost_breakdown: Dict[str, float]) -> Optional[float]:
    """
    GDC = sum of all cost items
    cost_breakdown: dict e.g., {"land": 50M, "construction": 120M, ...}
    """
    if not cost_breakdown:
        return None
    return sum(v for v in cost_breakdown.values() if v is not None)


def calculate_development_profit(gdv: Optional[float], gdc: Optional[float]) -> Optional[float]:
    """Development Profit = GDV - GDC"""
    if gdv is None or gdc is None:
        return None
    return gdv - gdc


def calculate_development_margin(gdv: Optional[float], gdc: Optional[float]) -> Optional[float]:
    """Development Margin % = (GDV - GDC) / GDV * 100"""
    if gdv is None or gdc is None or gdv == 0:
        return None
    return ((gdv - gdc) / gdv) * 100


def calculate_margin_on_cost(gdv: Optional[float], gdc: Optional[float]) -> Optional[float]:
    """Margin on Cost % = (GDV - GDC) / GDC * 100"""
    if gdv is None or gdc is None or gdc == 0:
        return None
    return ((gdv - gdc) / gdc) * 100


def calculate_cost_per_sqm(gdc: Optional[float], area: Optional[float]) -> Optional[float]:
    """Cost per SQM = GDC / Area (BUA or sellable — specify)"""
    if gdc is None or area is None or area == 0:
        return None
    return gdc / area


def calculate_price_per_sqm(gdv: Optional[float], sellable_area: Optional[float]) -> Optional[float]:
    """Price per SQM = GDV / Sellable Area"""
    if gdv is None or sellable_area is None or sellable_area == 0:
        return None
    return gdv / sellable_area


def calculate_profit_per_sqm(gdv: Optional[float], gdc: Optional[float], sellable_area: Optional[float]) -> Optional[float]:
    """Profit per SQM = (GDV - GDC) / Sellable Area"""
    if gdv is None or gdc is None or sellable_area is None or sellable_area == 0:
        return None
    return (gdv - gdc) / sellable_area


def calculate_land_cost_pct(land_cost: Optional[float], gdc: Optional[float]) -> Optional[float]:
    """Land Cost % = Land / GDC * 100"""
    if land_cost is None or gdc is None or gdc == 0:
        return None
    return (land_cost / gdc) * 100


def calculate_construction_cost_pct(construction_cost: Optional[float], gdc: Optional[float]) -> Optional[float]:
    """Construction % = Construction / GDC * 100"""
    if construction_cost is None or gdc is None or gdc == 0:
        return None
    return (construction_cost / gdc) * 100


def calculate_cost_ratio(cost_item: Optional[float], gdc: Optional[float]) -> Optional[float]:
    """Generic cost ratio % = Cost Item / GDC * 100"""
    if cost_item is None or gdc is None or gdc == 0:
        return None
    return (cost_item / gdc) * 100


def calculate_break_even_pct(gdc: Optional[float], gdv: Optional[float]) -> Optional[float]:
    """Break-even Sales % = GDC / GDV * 100"""
    if gdc is None or gdv is None or gdv == 0:
        return None
    return (gdc / gdv) * 100


def calculate_break_even_price(gdc: Optional[float], sellable_area: Optional[float], target_margin_pct: float = 0) -> Optional[float]:
    """
    Break-even Price per SQM = GDC * (1 + target_margin) / Sellable Area ? 
    Actually: if target_margin on GDV, then BE Price = (GDC / (1 - target_margin)) / Area
    Simplified: with 0 target, BE Price = GDC / Sellable Area
    With target margin m, BE Price = GDC / ((1 - m) * Area) — solving GDV*(1-m)=GDC
    """
    if gdc is None or sellable_area is None or sellable_area == 0:
        return None
    if target_margin_pct >= 100:
        return None
    divisor = (1 - target_margin_pct / 100) * sellable_area
    if divisor == 0:
        return None
    return gdc / divisor if target_margin_pct != 0 else gdc / sellable_area


def calculate_break_even_sales_value(gdc: Optional[float], target_profit: float = 0) -> Optional[float]:
    """Break-even Sales Value = GDC + Target Profit (simplified; exact is GDC if no target)"""
    if gdc is None:
        return None
    return gdc + target_profit


def calculate_safety_margin(gdv: Optional[float], break_even_sales: Optional[float]) -> Optional[float]:
    """Safety Margin % = (GDV - Break-even) / GDV * 100"""
    if gdv is None or break_even_sales is None or gdv == 0:
        return None
    return ((gdv - break_even_sales) / gdv) * 100


def calculate_residual_land_value(
    gdv: Optional[float],
    construction: Optional[float] = 0,
    soft_costs: Optional[float] = 0,
    marketing: Optional[float] = 0,
    financing: Optional[float] = 0,
    developer_profit: Optional[float] = 0,
    contingency: Optional[float] = 0,
    fees: Optional[float] = 0,
) -> Optional[float]:
    """
    Residual Land Value = GDV - (All costs except land + Developer Profit)
    """
    if gdv is None:
        return None
    total_deductions = sum(v or 0 for v in [construction, soft_costs, marketing, financing, developer_profit, contingency, fees])
    return gdv - total_deductions


def calculate_sales_rate(units_sold: Optional[int], total_units: Optional[int]) -> Optional[float]:
    """Sales Rate % = Units Sold / Total Units * 100"""
    if units_sold is None or total_units is None or total_units == 0:
        return None
    return (units_sold / total_units) * 100


def calculate_inventory_months(unsold_units: Optional[int], avg_monthly_sales: Optional[float]) -> Optional[float]:
    """Inventory Months = Unsold Units / Avg Monthly Sales"""
    if unsold_units is None or avg_monthly_sales is None or avg_monthly_sales == 0:
        return None
    return unsold_units / avg_monthly_sales


def calculate_collection_efficiency(collected: Optional[float], due: Optional[float]) -> Optional[float]:
    """Collection Efficiency % = Collected / Due * 100"""
    if collected is None or due is None or due == 0:
        return None
    return (collected / due) * 100
