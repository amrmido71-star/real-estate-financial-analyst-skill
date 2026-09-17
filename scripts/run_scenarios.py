#!/usr/bin/env python3
"""Wrapper: python scripts/run_scenarios.py --input project.json"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skill"))

from tools.model_runner import ModelRunner


def _load_assumptions():
    try:
        from examples.golden_project.assumptions import (
            best_case_delta,
            golden_assumptions,
            worst_case_delta,
        )

        return golden_assumptions, best_case_delta, worst_case_delta
    except ImportError:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "assumptions",
            str(
                pathlib.Path(__file__).resolve().parents[1]
                / "examples"
                / "golden_project"
                / "assumptions.py"
            ),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        return mod.golden_assumptions, mod.best_case_delta, mod.worst_case_delta


def main() -> None:
    golden_assumptions, best_case_delta, worst_case_delta = _load_assumptions()
    base_ass = golden_assumptions()
    runner = ModelRunner(base_ass)
    scenarios = runner.run_scenarios(best_case_delta(), worst_case_delta())
    for key, val in scenarios.items():
        if val is None:
            print(key, "None")
            continue
        irr = f"{val.equity_irr:.2%}" if val.equity_irr is not None else "N/A"
        print(key, f"profit {val.profit:,.0f}", f"margin {val.margin_pct:.1f}%", f"IRR {irr}")


if __name__ == "__main__":
    main()
