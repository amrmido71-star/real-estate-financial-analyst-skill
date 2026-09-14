"""
scenario_analysis.py — Scenario (Base/Best/Worst) & Sensitivity Analysis
"""

from typing import Optional, List, Dict, Callable
import copy

from .investment_metrics import calculate_irr, calculate_npv
from .project_metrics import calculate_gdv, calculate_gdc, calculate_development_margin


def run_scenarios(
    base_case: Dict,
    best_adjustments: Dict,
    worst_adjustments: Dict,
    calc_fn: Optional[Callable] = None,
) -> Dict[str, Dict]:
    """
    Generic scenario runner.
    base_case: dict with base assumptions e.g., {"gdv": 500M, "gdc": 350M, "cash_flows": [...]}
    best/worst_adjustments: dict of deltas to apply, e.g., {"gdv": 1.08, "gdc": 0.93} as multipliers
                            OR absolute overrides if key starts with "abs_"
                            Supported: numeric multipliers for gdv/gdc, or "cash_flows" list.
    calc_fn: optional function to compute metrics from scenario dict -> result dict.
             If None, uses built-in development metrics calculator.
    
    Returns: {"best": result_dict, "base": result_dict, "worst": result_dict}
    """
    def apply_adjustments(base: Dict, adjustments: Dict) -> Dict:
        scenario = copy.deepcopy(base)
        for key, adj in adjustments.items():
            if key.startswith("abs_"):
                real_key = key[4:]
                scenario[real_key] = adj
            elif key in scenario and isinstance(scenario[key], (int, float)) and isinstance(adj, (int, float)):
                # Multiplier: if adj between 0.5-1.5 treat as multiplier; else if >100 treat as absolute? 
                # We treat adj as multiplier if base is numeric and adj is reasonable multiplier
                # To disambiguate: caller should pass multiplier e.g., 1.08 for +8%
                scenario[key] = scenario[key] * adj
            elif key == "cash_flows" and isinstance(adj, list):
                scenario[key] = adj
            else:
                scenario[key] = adj
        return scenario

    base_result = calc_fn(base_case) if calc_fn else _default_calc(base_case)
    best_case = apply_adjustments(base_case, best_adjustments)
    worst_case = apply_adjustments(base_case, worst_adjustments)
    best_result = calc_fn(best_case) if calc_fn else _default_calc(best_case)
    worst_result = calc_fn(worst_case) if calc_fn else _default_calc(worst_case)

    return {
        "best": best_result,
        "base": base_result,
        "worst": worst_result,
    }


def _default_calc(scenario: Dict) -> Dict:
    """Default calc for development scenario with gdv, gdc, cash_flows, discount_rate"""
    gdv = scenario.get("gdv")
    gdc = scenario.get("gdc")
    cash_flows = scenario.get("cash_flows")
    discount_rate = scenario.get("discount_rate", 0.15)

    profit = None
    margin = None
    if gdv is not None and gdc is not None:
        profit = gdv - gdc
        margin = ((gdv - gdc) / gdv * 100) if gdv != 0 else None

    irr = None
    npv = None
    if cash_flows:
        irr = calculate_irr(cash_flows)
        npv = calculate_npv(cash_flows, discount_rate)

    return {
        "gdv": gdv,
        "gdc": gdc,
        "profit": profit,
        "margin_pct": margin,
        "irr": irr,
        "irr_pct": irr * 100 if irr is not None else None,
        "npv": npv,
        "cash_flows": cash_flows,
        "inputs": scenario,
    }


def run_sensitivity_analysis(
    base_case: Dict,
    variable: str,
    changes_pct: List[float],
    calc_fn: Optional[Callable] = None,
) -> List[Dict]:
    """
    One-variable-at-a-time sensitivity.
    variable: key in base_case to vary (e.g., "gdv", "gdc", "price", "cost")
    changes_pct: list of % changes e.g., [-10, -5, 0, 5, 10]
    Returns list of dicts: [{"change_pct": -10, "value": ..., "irr": ..., "npv": ..., "margin": ...}, ...]
    """
    results = []
    base_value = base_case.get(variable)
    if base_value is None:
        # If variable not in base_case, try to interpret generically
        for pct in changes_pct:
            scenario = copy.deepcopy(base_case)
            # Apply pct to gdv if variable suggests price
            if variable in ["price", "selling_price", "gdv"]:
                if base_case.get("gdv") is not None:
                    scenario["gdv"] = base_case["gdv"] * (1 + pct / 100)
            elif variable in ["cost", "construction", "gdc"]:
                if base_case.get("gdc") is not None:
                    scenario["gdc"] = base_case["gdc"] * (1 + pct / 100)
            # Also try direct
            if variable in scenario and isinstance(scenario[variable], (int, float)):
                # Already applied via gdv/gdc mapping, but ensure direct variable also scales
                pass
            res = calc_fn(scenario) if calc_fn else _default_calc(scenario)
            res["change_pct"] = pct
            res["variable"] = variable
            results.append(res)
        return results

    for pct in changes_pct:
        scenario = copy.deepcopy(base_case)
        if isinstance(base_value, (int, float)):
            scenario[variable] = base_value * (1 + pct / 100)
        elif isinstance(base_value, list):
            # For cash_flows, scale all positive flows? Simplified: scale entire series
            scenario[variable] = [cf * (1 + pct / 100) if cf > 0 else cf for cf in base_value]
        else:
            scenario[variable] = base_value

        res = calc_fn(scenario) if calc_fn else _default_calc(scenario)
        res["change_pct"] = pct
        res["variable"] = variable
        results.append(res)

    return results


def tornado_sensitivity(
    base_case: Dict,
    variables: List[str],
    change_pct: float = 10,
    metric: str = "irr_pct",
    calc_fn: Optional[Callable] = None,
) -> List[Dict]:
    """
    Tornado ranking: for each variable, compute metric at -change and +change vs base.
    Returns sorted list by spread descending (most sensitive first).
    """
    base_result = calc_fn(base_case) if calc_fn else _default_calc(base_case)
    base_metric = base_result.get(metric)

    tornado = []
    for var in variables:
        # -change
        neg_results = run_sensitivity_analysis(base_case, var, [-change_pct], calc_fn=calc_fn)
        pos_results = run_sensitivity_analysis(base_case, var, [change_pct], calc_fn=calc_fn)
        neg_val = neg_results[0].get(metric) if neg_results else None
        pos_val = pos_results[0].get(metric) if pos_results else None

        spread = None
        if neg_val is not None and pos_val is not None:
            spread = abs(pos_val - neg_val)
        elif neg_val is not None and base_metric is not None:
            spread = abs(neg_val - base_metric)
        elif pos_val is not None and base_metric is not None:
            spread = abs(pos_val - base_metric)

        tornado.append({
            "variable": var,
            "base": base_metric,
            "down": neg_val,
            "up": pos_val,
            "spread": spread,
        })

    # Sort by spread descending, None last
    tornado.sort(key=lambda x: (x["spread"] is not None, x["spread"] or 0), reverse=True)
    return tornado


def format_scenario_table(scenarios: Dict[str, Dict], metrics: List[str] = None) -> str:
    """Format scenario comparison as markdown table string"""
    if metrics is None:
        metrics = ["gdv", "gdc", "profit", "margin_pct", "irr_pct", "npv"]
    header = "| Metric | Best | Base | Worst |"
    separator = "|--------|-----:|-----:|------:|"
    rows = [header, separator]
    for m in metrics:
        best = scenarios.get("best", {}).get(m, "N/A")
        base = scenarios.get("base", {}).get(m, "N/A")
        worst = scenarios.get("worst", {}).get(m, "N/A")
        # Format numbers
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
