"""scenario_engine.py — Scenario, sensitivity, tornado, Monte Carlo (optional)"""
from typing import List, Dict
from ..scenario_analysis import run_scenarios, run_sensitivity_analysis, run_two_way_sensitivity, tornado_sensitivity

class ScenarioEngine:
    @staticmethod
    def scenarios(base, best, worst, calc_fn=None):
        return run_scenarios(base, best, worst, calc_fn)

    @staticmethod
    def sensitivity(base, variable: str, changes: List[float], calc_fn=None):
        return run_sensitivity_analysis(base, variable, changes, calc_fn)

    @staticmethod
    def two_way(base, var1: str, changes1: List[float], var2: str, changes2: List[float], metric: str = "irr_pct"):
        return run_two_way_sensitivity(base, var1, changes1, var2, changes2, metric)

    @staticmethod
    def tornado(base, variables: List[str], pct: float = 10, metric: str = "irr_pct"):
        return tornado_sensitivity(base, variables, pct, metric)

    @staticmethod
    def monte_carlo(base_case: Dict, variables: Dict, iterations: int = 1000, metric: str = "npv", seed: int = 42):
        """
        Optional Monte Carlo: variables = {"selling_price":{"dist":"normal","mean":0,"std":10}, ...}
        For each iteration, sample each variable and rebuild.
        Returns P10/P50/P90 and prob metrics.
        If not needed, this is feature-flagged.
        """
        import random
        random.seed(seed)
        results = []
        from ..scenario_analysis import _rebuild_financials
        for _ in range(iterations):
            assumptions = {}
            for var, cfg in variables.items():
                dist = cfg.get("dist", "normal")
                mean = cfg.get("mean", 0)
                std = cfg.get("std", 5)
                if dist == "normal":
                    sample = random.gauss(mean, std)
                elif dist == "triangular":
                    low = cfg.get("low", mean-10)
                    mode = cfg.get("mode", mean)
                    high = cfg.get("high", mean+10)
                    sample = random.triangular(low, high, mode)
                elif dist == "uniform":
                    low = cfg.get("low", mean-10)
                    high = cfg.get("high", mean+10)
                    sample = random.uniform(low, high)
                else:
                    sample = mean
                # Map var to assumption key
                key_map = {"selling_price":"selling_price_change_pct","construction_cost":"construction_cost_change_pct","delay":"delay_months","interest":"interest_rate_delta","collection_rate":"collection_rate_change_pct"}
                assumptions[key_map.get(var, var)] = sample
            res = _rebuild_financials(base_case, assumptions)
            val = res.get(metric)
            if val is not None:
                results.append(val)
        if not results:
            return {"p10": None, "p50": None, "p90": None}
        results_sorted = sorted(results)
        n = len(results_sorted)
        def pct(p): return results_sorted[int(n*p/100)]
        p10 = pct(10)
        p50 = pct(50)
        p90 = pct(90)
        prob_negative = sum(1 for v in results if v < 0)/n if metric in ["npv","profit"] else None
        return {
            "iterations": iterations,
            "p10": p10,
            "p50": p50,
            "p90": p90,
            "mean": sum(results)/n,
            "prob_negative_npv": prob_negative,
            "samples": results[:5],  # preview
        }
