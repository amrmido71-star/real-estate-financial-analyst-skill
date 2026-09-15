"""model_runner.py — Runner for Integrated Model: scenarios, sensitivity, portfolio"""
from typing import List, Dict, Optional
from .integrated_model import IntegratedRealEstateModel
from .models.assumptions import ProjectAssumptions

class ModelRunner:
    """Orchestrates multiple runs: base, scenarios, sensitivity"""
    def __init__(self, base_assumptions: ProjectAssumptions):
        self.base = base_assumptions

    def run_base(self):
        model = IntegratedRealEstateModel(self.base)
        return model.run()

    def run_scenarios(self, best_assumptions: Optional[Dict] = None, worst_assumptions: Optional[Dict] = None, stress_assumptions: Optional[Dict] = None):
        # Best/Worst are assumption deltas dicts, not full assumptions
        # We need to apply deltas to base
        from copy import deepcopy
        def apply_delta(delta: Dict) -> ProjectAssumptions:
            new = deepcopy(self.base)
            # Map delta keys to assumptions
            if "selling_price_change_pct" in delta:
                pct = delta["selling_price_change_pct"]
                new.product.avg_price_per_sqm = self.base.product.avg_price_per_sqm * (1 + pct/100)
            if "construction_cost_change_pct" in delta:
                pct = delta["construction_cost_change_pct"]
                new.construction.budget = self.base.construction.budget * (1 + pct/100)
            if "sales_velocity_change_pct" in delta:
                pct = delta["sales_velocity_change_pct"]
                new.sales.velocity_units_per_month = self.base.sales.velocity_units_per_month * (1 + pct/100)
            if "collection_rate_change_pct" in delta:
                # delta is change in rate points? e.g., -10 => 90*0.9=81?
                # For simplicity, treat as pct of rate
                pct = delta["collection_rate_change_pct"]
                new.collections.collection_rate_pct = self.base.collections.collection_rate_pct * (1 + pct/100)
            if "interest_rate_delta" in delta:
                new.financing.interest_rate_annual_pct = self.base.financing.interest_rate_annual_pct + delta["interest_rate_delta"]
            if "delay_months" in delta:
                new.construction.duration_months = self.base.construction.duration_months + delta["delay_months"]
            return new

        base_result = self.run_base()
        best = IntegratedRealEstateModel(apply_delta(best_assumptions)).run() if best_assumptions else None
        worst = IntegratedRealEstateModel(apply_delta(worst_assumptions)).run() if worst_assumptions else None
        stress = IntegratedRealEstateModel(apply_delta(stress_assumptions)).run() if stress_assumptions else None

        return {"base": base_result, "best": best, "worst": worst, "stress": stress}

    def sensitivity(self, variable: str, changes: List[float]):
        """One-way sensitivity: returns list of results"""
        from copy import deepcopy
        results = []
        for ch in changes:
            new = deepcopy(self.base)
            if variable == "selling_price":
                new.product.avg_price_per_sqm = self.base.product.avg_price_per_sqm * (1 + ch/100)
            elif variable == "construction_cost":
                new.construction.budget = self.base.construction.budget * (1 + ch/100)
            elif variable == "sales_velocity":
                new.sales.velocity_units_per_month = self.base.sales.velocity_units_per_month * (1 + ch/100)
            elif variable == "collection_rate":
                new.collections.collection_rate_pct = self.base.collections.collection_rate_pct * (1 + ch/100)
            elif variable == "interest_rate":
                new.financing.interest_rate_annual_pct = self.base.financing.interest_rate_annual_pct + ch
            elif variable == "delay":
                new.construction.duration_months = self.base.construction.duration_months + int(ch)
            res = IntegratedRealEstateModel(new).run()
            results.append({"change": ch, "result": res})
        return results

    def two_way(self, var1: str, changes1: List[float], var2: str, changes2: List[float], metric: str = "equity_irr"):
        matrix = []
        for c1 in changes1:
            row = []
            for c2 in changes2:
                # same as above but combine
                from copy import deepcopy
                new = deepcopy(self.base)
                # apply var1
                if var1 == "selling_price":
                    new.product.avg_price_per_sqm = self.base.product.avg_price_per_sqm * (1 + c1/100)
                elif var1 == "construction_cost":
                    new.construction.budget = self.base.construction.budget * (1 + c1/100)
                if var2 == "selling_price":
                    new.product.avg_price_per_sqm = self.base.product.avg_price_per_sqm * (1 + c2/100) if var1 != "selling_price" else new.product.avg_price_per_sqm
                elif var2 == "construction_cost":
                    new.construction.budget = self.base.construction.budget * (1 + c2/100) if var1 != "construction_cost" else new.construction.budget
                # For other combos, simplistic
                res = IntegratedRealEstateModel(new).run()
                val = getattr(res, metric, None)
                # Try dashboard returns
                if val is None and hasattr(res, "dashboard"):
                    val = res.dashboard["returns"].get(metric)
                row.append(val)
            matrix.append(row)
        return {"var1": var1, "var2": var2, "changes1": changes1, "changes2": changes2, "metric": metric, "matrix": matrix}
