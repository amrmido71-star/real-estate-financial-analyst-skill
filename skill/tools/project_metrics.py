"""
project_metrics.py — Real Estate Development Project Metrics
GDV, GDC, Margins, per-SQM, Cost Ratios, Break-even
Break-even definitions are unified:
  Target Margin = Profit / Revenue  =>  Revenue = Cost / (1 - TargetMargin)
"""

from typing import Optional, List, Dict


def calculate_gdv(units: List[Dict]) -> Optional[float]:
    if not units:
        return None
    total = 0.0
    for u in units:
        qty = u.get("units", u.get("quantity", u.get("count", 0)))
        price = u.get("price_per_unit", u.get("price", u.get("selling_price", 0)))
        total += qty * price
    return total


def calculate_gdv_from_area(sellable_area: Optional[float], price_per_sqm: Optional[float]) -> Optional[float]:
    if sellable_area is None or price_per_sqm is None:
        return None
    return sellable_area * price_per_sqm


def calculate_gdc(cost_breakdown: Dict[str, float]) -> Optional[float]:
    if not cost_breakdown:
        return None
    return sum(v for v in cost_breakdown.values() if v is not None)


def calculate_development_profit(gdv: Optional[float], gdc: Optional[float]) -> Optional[float]:
    if gdv is None or gdc is None:
        return None
    return gdv - gdc


def calculate_development_margin(gdv: Optional[float], gdc: Optional[float]) -> Optional[float]:
    """Development Margin % = (GDV - GDC) / GDV * 100"""
    if gdv is None or gdc is None or gdv == 0:
        return None
    return ((gdv - gdc) / gdv) * 100


def calculate_margin_on_cost(gdv: Optional[float], gdc: Optional[float]) -> Optional[float]:
    if gdv is None or gdc is None or gdc == 0:
        return None
    return ((gdv - gdc) / gdc) * 100


def calculate_cost_per_sqm(gdc: Optional[float], area: Optional[float]) -> Optional[float]:
    if gdc is None or area is None or area == 0:
        return None
    return gdc / area


def calculate_price_per_sqm(gdv: Optional[float], sellable_area: Optional[float]) -> Optional[float]:
    if gdv is None or sellable_area is None or sellable_area == 0:
        return None
    return gdv / sellable_area


def calculate_profit_per_sqm(gdv: Optional[float], gdc: Optional[float], sellable_area: Optional[float]) -> Optional[float]:
    if gdv is None or gdc is None or sellable_area is None or sellable_area == 0:
        return None
    return (gdv - gdc) / sellable_area


def calculate_land_cost_pct(land_cost: Optional[float], gdc: Optional[float]) -> Optional[float]:
    if land_cost is None or gdc is None or gdc == 0:
        return None
    return (land_cost / gdc) * 100


def calculate_construction_cost_pct(construction_cost: Optional[float], gdc: Optional[float]) -> Optional[float]:
    if construction_cost is None or gdc is None or gdc == 0:
        return None
    return (construction_cost / gdc) * 100


def calculate_cost_ratio(cost_item: Optional[float], gdc: Optional[float]) -> Optional[float]:
    if cost_item is None or gdc is None or gdc == 0:
        return None
    return (cost_item / gdc) * 100


# ---- Break-even (unified definitions) ----

def calculate_break_even_pct(gdc: Optional[float], gdv: Optional[float]) -> Optional[float]:
    """
    Break-even Sales % = GDC / GDV * 100
    At 0% target margin. This is the % of GDV that must be sold to cover costs.
    """
    if gdc is None or gdv is None or gdv == 0:
        return None
    return (gdc / gdv) * 100


def calculate_break_even_revenue(gdc: Optional[float], target_margin_pct: float = 0) -> Optional[float]:
    """
    Break-even Revenue (or Required Revenue) for a given target margin.
    Definition: Target Margin = Profit / Revenue  =>  Revenue = Cost / (1 - TargetMargin)
    - target_margin_pct=0 => Revenue = GDC (true break-even)
    - target_margin_pct=20 => Revenue = GDC / 0.8 (need 25% more revenue to achieve 20% margin)
    Returns None if target_margin_pct >=100 or < -100? Allow negative margin but guard >=100.
    """
    if gdc is None:
        return None
    if target_margin_pct >= 100:
        return None
    if target_margin_pct <= -100:
        # -100% margin means revenue = cost/2, allowed but rare
        pass
    divisor = 1 - target_margin_pct / 100
    if divisor == 0:
        return None
    return gdc / divisor


def calculate_break_even_price(gdc: Optional[float], sellable_area: Optional[float], target_margin_pct: float = 0) -> Optional[float]:
    """
    Break-even Price per SQM = Required Revenue / Sellable Area
    Where Required Revenue = GDC / (1 - TargetMargin)
    - target_margin_pct=0 => Price = GDC / Area (true break-even)
    - target_margin_pct=20 => Price = (GDC/0.8)/Area
    """
    if gdc is None or sellable_area is None or sellable_area == 0:
        return None
    if target_margin_pct >= 100:
        return None
    required_revenue = calculate_break_even_revenue(gdc, target_margin_pct)
    if required_revenue is None:
        return None
    return required_revenue / sellable_area


def calculate_break_even_sales_value(gdc: Optional[float], target_profit: float = 0) -> Optional[float]:
    """Break-even Sales Value = GDC + Target Profit (profit-based, not margin-based)"""
    if gdc is None:
        return None
    return gdc + target_profit


def calculate_break_even_units(gdc: Optional[float], price_per_unit: Optional[float], target_margin_pct: float = 0) -> Optional[float]:
    """Break-even Units = Required Revenue / Price per Unit"""
    if gdc is None or price_per_unit is None or price_per_unit == 0:
        return None
    rev = calculate_break_even_revenue(gdc, target_margin_pct)
    if rev is None:
        return None
    return rev / price_per_unit


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
    if gdv is None:
        return None
    total_deductions = sum(v or 0 for v in [construction, soft_costs, marketing, financing, developer_profit, contingency, fees])
    return gdv - total_deductions


def calculate_sales_rate(units_sold: Optional[int], total_units: Optional[int]) -> Optional[float]:
    if units_sold is None or total_units is None or total_units == 0:
        return None
    return (units_sold / total_units) * 100


def calculate_inventory_months(unsold_units: Optional[int], avg_monthly_sales: Optional[float]) -> Optional[float]:
    if unsold_units is None or avg_monthly_sales is None or avg_monthly_sales == 0:
        return None
    return unsold_units / avg_monthly_sales


def calculate_collection_efficiency(collected: Optional[float], due: Optional[float]) -> Optional[float]:
    if collected is None or due is None or due == 0:
        return None
    return (collected / due) * 100
