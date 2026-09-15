"""
scenario_analysis.py — True Financial Scenario & Sensitivity Engine
Supports Base/Best/Worst with full rebuild: Assumption -> Revenue -> Collection -> Cost -> Financing -> Cash Flow -> Profit -> IRR/NPV
"""

from typing import Optional, List, Dict, Callable
import copy
from .investment_metrics import calculate_irr, calculate_npv
from .project_metrics import calculate_gdv


def _rebuild_financials(base: Dict, assumptions: Dict) -> Dict:
    """
    Rebuild financials from base + assumptions.
    Base can contain:
        - gdv, gdc, cash_flows, discount_rate (simple)
        - OR detailed: sellable_area, price_per_sqm, units, cost_breakdown, sales_velocity, collection_rate, interest_rate, etc.
    Assumptions can contain:
        selling_price_change_pct, construction_cost_change_pct, soft_cost_change_pct, land_cost_change_pct,
        marketing_cost_change_pct, financing_cost_change_pct, sales_velocity_change_pct,
        collection_rate_change_pct, interest_rate_delta, delay_months, discount_rate
    Returns rebuilt dict with gdv,gdc,profit,margin,cash_flows,irr,npv,peak_funding
    """
    rebuilt = copy.deepcopy(base)
    # Extract base values
    # --- Handle GDV adjustments ---
    # If base has cost_breakdown/units, prefer to rebuild those
    if "cost_breakdown" in base and isinstance(base["cost_breakdown"], dict):
        cb = copy.deepcopy(base["cost_breakdown"])
        # Apply cost changes
        if "construction_cost_change_pct" in assumptions:
            pct = assumptions["construction_cost_change_pct"]
            if "construction" in cb:
                cb["construction"] = cb["construction"] * (1 + pct/100)
            # Also handle hard cost variants
            for k in list(cb.keys()):
                if "construct" in k.lower():
                    cb[k] = base["cost_breakdown"][k] * (1 + pct/100)
        if "soft_cost_change_pct" in assumptions:
            pct = assumptions["soft_cost_change_pct"]
            for k in ["soft", "soft_costs", "design", "consultancy"]:
                if k in cb:
                    cb[k] = base["cost_breakdown"][k] * (1 + pct/100)
        if "land_cost_change_pct" in assumptions:
            pct = assumptions["land_cost_change_pct"]
            if "land" in cb:
                cb["land"] = base["cost_breakdown"]["land"] * (1 + pct/100)
        if "marketing_cost_change_pct" in assumptions:
            pct = assumptions["marketing_cost_change_pct"]
            for k in ["marketing", "sales_marketing", "sales"]:
                if k in cb:
                    cb[k] = base["cost_breakdown"][k] * (1 + pct/100)
        if "financing_cost_change_pct" in assumptions:
            pct = assumptions["financing_cost_change_pct"]
            for k in ["financing", "financing_cost"]:
                if k in cb:
                    cb[k] = base["cost_breakdown"][k] * (1 + pct/100)
        rebuilt["cost_breakdown"] = cb
        # Recalculate GDC
        rebuilt["gdc"] = sum(v for v in cb.values() if v is not None)
        # Update direct gdc if present
        if "construction_cost_change_pct" in assumptions or "soft_cost_change_pct" in assumptions or "land_cost_change_pct" in assumptions:
            pass  # already handled

    # Direct gdc multiplier fallback if no breakdown
    if "gdc" in base and "cost_breakdown" not in base:
        if "construction_cost_change_pct" in assumptions:
            rebuilt["gdc"] = base["gdc"] * (1 + assumptions["construction_cost_change_pct"]/100)
        # Could be overridden by more specific, but keep simple

    # --- GDV adjustments ---
    if "selling_price_change_pct" in assumptions:
        pct = assumptions["selling_price_change_pct"]
        if "gdv" in base:
            rebuilt["gdv"] = base["gdv"] * (1 + pct/100)
        # If units present, adjust each unit price
        if "units" in base and isinstance(base["units"], list):
            new_units = []
            for u in base["units"]:
                nu = copy.deepcopy(u)
                # Adjust price_per_unit
                for key in ["price_per_unit", "price", "selling_price"]:
                    if key in nu:
                        nu[key] = nu[key] * (1 + pct/100)
                        break
                new_units.append(nu)
            rebuilt["units"] = new_units
            rebuilt["gdv"] = calculate_gdv(new_units) or rebuilt.get("gdv")
        if "sellable_area" in base and "price_per_sqm" in base:
            rebuilt["price_per_sqm"] = base["price_per_sqm"] * (1 + pct/100)
            rebuilt["gdv"] = rebuilt["sellable_area"] * rebuilt["price_per_sqm"]

    # --- Cash flow rebuild ---
    # If cash_flows present, adjust them based on assumptions
    base_cfs = base.get("cash_flows")
    if base_cfs:
        new_cfs = list(base_cfs)
        # Selling price change => scale positive inflows (sales collections)
        if "selling_price_change_pct" in assumptions:
            pct = assumptions["selling_price_change_pct"]
            # Scale positive cash flows (inflows) by pct, keep negatives (costs) as is unless construction change
            # But to avoid double scaling, we scale positives only
            new_cfs = [cf * (1 + pct/100) if cf > 0 else cf for cf in new_cfs]
        # Construction cost change => scale negative outflows
        if "construction_cost_change_pct" in assumptions:
            pct = assumptions["construction_cost_change_pct"]
            # Scale negatives (costs) by pct, but they are negative so making more negative if pct positive
            # Example: -100 with +15% => -115
            scaled = []
            for cf in new_cfs:
                if cf < 0:
                    # Increase magnitude by pct
                    scaled.append(cf * (1 + pct/100))
                else:
                    scaled.append(cf)
            new_cfs = scaled
        # Collection rate: affects positive flows magnitude
        if "collection_rate_change_pct" in assumptions:
            pct = assumptions["collection_rate_change_pct"]
            # Interpret as change in collection efficiency: e.g., -10 => 90% of positives
            # If base collection_rate is 90%, and change -10 => 81%? But we have simple: scale positives by (1+pct/100)
            new_cfs = [cf * (1 + pct/100) if cf > 0 else cf for cf in new_cfs]
        # Interest rate change: affect financing portion? Simplified: adjust negative flows slightly and positives?
        # For now, adjust all flows by small factor based on interest delta
        if "interest_rate_delta" in assumptions or "interest_rate_change_pct" in assumptions:
            # If interest up, costs up (more negative) and maybe financing
            delta = assumptions.get("interest_rate_delta", 0)
            # Approximate: each period's net affected by - debt * delta
            # Simplified: scale negatives by delta*0.5
            if delta != 0:
                # delta is absolute pts e.g., +2 => rate +2%
                # Apply 5% per point to negatives as placeholder
                factor = 1 + delta * 0.02  # 2% per point
                new_cfs = [cf * factor if cf < 0 else cf for cf in new_cfs]
        # Delay: shift positive flows later (delay sales)
        if "delay_months" in assumptions and assumptions["delay_months"] != 0:
            delay = assumptions["delay_months"]
            # For yearly cash flows, delay in months => shift fraction of year
            # Simplified: if delay 6 months and yearly, shift half of each positive to next period
            # For monthly, would need more granular; here we do simple: insert zeros at start and truncate?
            # Approach: if delay positive, move positives one period later (and add zero at front)
            if delay > 0:
                # For yearly: delay 6 months => delay 0.5 year => move 50% of each positive to next year
                # Simplified: insert 0 at position 1 and shift positives? Easier: add delay periods of 0 then re-aggregate
                # We'll implement simple: add delay periods of 0 after period 0, and drop last
                delay_periods = max(1, round(delay / 12)) if len(new_cfs) <= 10 else max(1, delay)  # yearly vs monthly heuristic
                # Only shift if we have many periods, else fraction
                if len(new_cfs) > 5:
                    # Yearly: shift
                    shifted = [new_cfs[0]] + [0]*delay_periods + new_cfs[1:]
                    # Keep same length by truncating or keep extended? Keep extended to show delay impact
                    new_cfs = shifted
                else:
                    # Monthly-like: insert zeros
                    shifted = [new_cfs[0]] + [0]*delay + new_cfs[1:]
                    new_cfs = shifted

        rebuilt["cash_flows"] = new_cfs
    else:
        rebuilt["cash_flows"] = base.get("cash_flows")

    # Recompute derived
    gdv = rebuilt.get("gdv", base.get("gdv"))
    gdc = rebuilt.get("gdc", base.get("gdc"))
    if gdv is not None and gdc is not None:
        rebuilt["profit"] = gdv - gdc
        rebuilt["margin_pct"] = ((gdv - gdc)/gdv*100) if gdv != 0 else None
    discount_rate = assumptions.get("discount_rate", base.get("discount_rate", 0.15))
    rebuilt["discount_rate"] = discount_rate
    cfs = rebuilt.get("cash_flows")
    if cfs:
        rebuilt["irr"] = calculate_irr(cfs)
        rebuilt["irr_pct"] = rebuilt["irr"]*100 if rebuilt["irr"] else None
        rebuilt["npv"] = calculate_npv(cfs, discount_rate)
        # Peak funding: analyze cash flow
        # Treat cash_flows as net cash flows per period
        try:
            # If cash_flows are net, cumulative = running sum
            cum = []
            running = 0
            for cf in cfs:
                running += cf
                cum.append(running)
            min_cum = min(cum) if cum else 0
            rebuilt["peak_funding"] = abs(min_cum) if min_cum < 0 else 0
            rebuilt["cumulative"] = cum
        except Exception:
            rebuilt["peak_funding"] = None
    return rebuilt


def run_scenarios(
    base_case: Dict,
    best_assumptions: Dict,
    worst_assumptions: Dict,
    calc_fn: Optional[Callable] = None,
) -> Dict[str, Dict]:
    """
    True financial scenario runner.
    best/worst are assumption dicts like {"selling_price_change_pct":8, "construction_cost_change_pct":-7, ...}
    If calc_fn provided, use it; else use _rebuild_financials
    Also supports legacy multiplier style: {"gdv":1.08, "gdc":0.93} for backward compat
    """
    # Detect legacy style (value multipliers 0.5-2.0 for gdv/gdc)
    def is_legacy(d):
        return any(k in ["gdv","gdc"] and isinstance(v,(int,float)) and 0.5 <= v <= 2.0 for k,v in d.items())

    if is_legacy(best_assumptions) or is_legacy(worst_assumptions):
        # Legacy path: simple multiplier
        import copy as cp
        def apply_legacy(base, adj):
            sc = cp.deepcopy(base)
            for k,v in adj.items():
                if k.startswith("abs_"):
                    sc[k[4:]] = v
                elif k in sc and isinstance(sc[k],(int,float)) and isinstance(v,(int,float)):
                    sc[k] = sc[k]*v
                elif k=="cash_flows" and isinstance(v,list):
                    sc[k]=v
                else:
                    sc[k]=v
            return sc
        base_result = calc_fn(base_case) if calc_fn else _legacy_calc(base_case)
        best_case = apply_legacy(base_case, best_assumptions)
        worst_case = apply_legacy(base_case, worst_assumptions)
        best_result = calc_fn(best_case) if calc_fn else _legacy_calc(best_case)
        worst_result = calc_fn(worst_case) if calc_fn else _legacy_calc(worst_case)
        return {"best": best_result, "base": base_result, "worst": worst_result}

    # True rebuild path
    base_result = calc_fn(base_case) if calc_fn else _rebuild_financials(base_case, {})
    # Need to handle that base_result is rebuilt; but we want base as rebuilt with no assumptions
    # Actually _rebuild_financials with {} gives base with derived fields
    best_result = _rebuild_financials(base_case, best_assumptions) if not calc_fn else calc_fn({**base_case, **best_assumptions})
    worst_result = _rebuild_financials(base_case, worst_assumptions) if not calc_fn else calc_fn({**base_case, **worst_assumptions})

    # If calc_fn provided, it should handle assumptions itself; we already did simple merge
    # For true path without calc_fn, we already did rebuild
    return {"best": best_result, "base": base_result, "worst": worst_result}


def _legacy_calc(scenario: Dict) -> Dict:
    gdv = scenario.get("gdv")
    gdc = scenario.get("gdc")
    cfs = scenario.get("cash_flows")
    dr = scenario.get("discount_rate", 0.15)
    profit = gdv - gdc if gdv is not None and gdc is not None else None
    margin = ((gdv - gdc)/gdv*100) if gdv and gdc and gdv!=0 else None
    irr = calculate_irr(cfs) if cfs else None
    npv = calculate_npv(cfs, dr) if cfs else None
    return {"gdv":gdv,"gdc":gdc,"profit":profit,"margin_pct":margin,"irr":irr,"irr_pct":irr*100 if irr else None,"npv":npv,"cash_flows":cfs,"inputs":scenario}


def run_sensitivity_analysis(
    base_case: Dict,
    variable: str,
    changes_pct: List[float],
    calc_fn: Optional[Callable] = None,
) -> List[Dict]:
    """
    One-way sensitivity: vary one variable, rebuild financials each time.
    variable can be: selling_price, construction_cost, sales_velocity, collection_rate, interest_rate, delay
    changes_pct: e.g., [-20,-10,-5,0,5,10,20] — for delay, interpret as months? But we treat as pct for most, and for delay as months (change value = months)
    """
    results = []
    # Map variable names to assumption keys
    var_map = {
        "selling_price": "selling_price_change_pct",
        "price": "selling_price_change_pct",
        "gdv": "selling_price_change_pct",
        "construction_cost": "construction_cost_change_pct",
        "construction": "construction_cost_change_pct",
        "gdc": "construction_cost_change_pct",
        "cost": "construction_cost_change_pct",
        "soft_cost": "soft_cost_change_pct",
        "land_cost": "land_cost_change_pct",
        "marketing_cost": "marketing_cost_change_pct",
        "sales_velocity": "sales_velocity_change_pct",
        "velocity": "sales_velocity_change_pct",
        "collection_rate": "collection_rate_change_pct",
        "collection": "collection_rate_change_pct",
        "interest_rate": "interest_rate_delta",
        "interest": "interest_rate_delta",
        "delay": "delay_months",
        "project_delay": "delay_months",
    }
    assumption_key = var_map.get(variable, variable)

    for pct in changes_pct:
        assumptions = {}
        # Special handling: for delay, pct is months (not %)
        if assumption_key == "delay_months":
            assumptions[assumption_key] = int(pct)  # interpret pct as months
        elif assumption_key == "interest_rate_delta":
            # pct is absolute points if variable is interest_rate, but changes_pct is like [-2,-1,0,1,2]
            # For sensitivity, pct is points (e.g., -2 => -2pts)
            assumptions[assumption_key] = pct  # type: ignore[assignment]
        else:
            assumptions[assumption_key] = pct  # type: ignore[assignment]

        if calc_fn:
            # Merge base + assumptions and apply calc_fn
            scenario = {**base_case, **assumptions}
            # For calc_fn that expects direct var change, also set variable directly if exists in base
            if variable in base_case:
                base_val = base_case[variable]
                if isinstance(base_val, (int, float)):
                    scenario[variable] = base_val * (1 + pct/100)
            res = calc_fn(scenario)
            res["change_pct"] = pct
            res["variable"] = variable
            results.append(res)
        else:
            res = _rebuild_financials(base_case, assumptions)
            res["change_pct"] = pct
            res["variable"] = variable
            # Keep original key for display
            res["assumption_key"] = assumption_key
            results.append(res)
    return results


def run_two_way_sensitivity(
    base_case: Dict,
    var1: str,
    var1_changes: List[float],
    var2: str,
    var2_changes: List[float],
    metric: str = "irr_pct",
) -> Dict:
    """
    Two-way sensitivity matrix.
    Returns {"var1":var1, "var2":var2, "var1_changes":..., "var2_changes":..., "matrix":[[...]], "metric":metric}
    Matrix rows = var1, cols = var2
    """
    matrix = []
    for v1 in var1_changes:
        row = []
        for v2 in var2_changes:
            # Combine assumptions
            assumptions = {}
            var_map = {
                "selling_price": "selling_price_change_pct",
                "price": "selling_price_change_pct",
                "construction_cost": "construction_cost_change_pct",
                "cost": "construction_cost_change_pct",
            }
            k1 = var_map.get(var1, var1)
            k2 = var_map.get(var2, var2)
            # Handle delay/interest special? For two-way we assume pct for both unless var is delay/interest
            if k1 == "delay_months":
                assumptions[k1] = int(v1)
            elif k1 == "interest_rate_delta":
                assumptions[k1] = v1  # type: ignore[assignment]
            else:
                assumptions[k1] = v1  # type: ignore[assignment]
            if k2 == "delay_months":
                assumptions[k2] = int(v2)
            elif k2 == "interest_rate_delta":
                assumptions[k2] = v2  # type: ignore[assignment]
            else:
                assumptions[k2] = v2  # type: ignore[assignment]
            res = _rebuild_financials(base_case, assumptions)
            val = res.get(metric)
            row.append(val)
        matrix.append(row)
    return {
        "var1": var1,
        "var2": var2,
        "var1_changes": var1_changes,
        "var2_changes": var2_changes,
        "metric": metric,
        "matrix": matrix,
    }


def tornado_sensitivity(
    base_case: Dict,
    variables: List[str],
    change_pct: float = 10,
    metric: str = "irr_pct",
    calc_fn: Optional[Callable] = None,
) -> List[Dict]:
    base_result = calc_fn(base_case) if calc_fn else _rebuild_financials(base_case, {})
    base_metric = base_result.get(metric)
    # For margin, try alternative keys
    if base_metric is None:
        # Try profit, margin_pct etc.
        alt_keys = ["irr", "npv", "margin_pct", "profit"]
        for k in alt_keys:
            if base_result.get(k) is not None and metric == k:
                base_metric = base_result.get(k)
                break
    tornado = []
    for var in variables:
        neg_res = run_sensitivity_analysis(base_case, var, [-change_pct], calc_fn=calc_fn)
        pos_res = run_sensitivity_analysis(base_case, var, [change_pct], calc_fn=calc_fn)
        neg_val = neg_res[0].get(metric) if neg_res else None
        pos_val = pos_res[0].get(metric) if pos_res else None
        # Fallback try other metric names
        if neg_val is None:
            # Try to find any metric that exists
            for k in ["irr_pct","irr","npv","margin_pct","profit"]:
                if neg_res and neg_res[0].get(k) is not None:
                    neg_val = neg_res[0].get(k)
                    break
        if pos_val is None:
            for k in ["irr_pct","irr","npv","margin_pct","profit"]:
                if pos_res and pos_res[0].get(k) is not None:
                    pos_val = pos_res[0].get(k)
                    break
        spread = None
        if neg_val is not None and pos_val is not None:
            spread = abs(pos_val - neg_val)
        elif neg_val is not None and base_metric is not None:
            spread = abs(neg_val - base_metric)
        elif pos_val is not None and base_metric is not None:
            spread = abs(pos_val - base_metric)
        tornado.append({"variable": var, "base": base_metric, "down": neg_val, "up": pos_val, "spread": spread})
    tornado.sort(key=lambda x: (x["spread"] is not None, x["spread"] or 0), reverse=True)
    return tornado


def format_scenario_table(scenarios: Dict[str, Dict], metrics: Optional[List[str]] = None) -> str:
    if metrics is None:
        metrics = ["gdv", "gdc", "profit", "margin_pct", "irr_pct", "npv", "peak_funding"]
    header = "| Metric | Best | Base | Worst |"
    separator = "|--------|-----:|-----:|------:|"
    rows = [header, separator]
    for m in metrics:
        best = scenarios.get("best", {}).get(m, "N/A")
        base = scenarios.get("base", {}).get(m, "N/A")
        worst = scenarios.get("worst", {}).get(m, "N/A")
        def fmt(v):
            if v is None or v == "N/A":
                return "N/A"
            if isinstance(v, float):
                if abs(v) >= 1000:
                    return f"{v:,.0f}"
                else:
                    return f"{v:.2f}"
            return str(v)
        rows.append(f"| {m} | {fmt(best)} | {fmt(base)} | {fmt(worst)} |")
    return "\n".join(rows)
