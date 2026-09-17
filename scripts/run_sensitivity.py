#!/usr/bin/env python3
"""Wrapper: python scripts/run_sensitivity.py --input project.json --variable selling_price"""

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skill"))

from tools.model_runner import ModelRunner
from tools.scenario_analysis import run_sensitivity_analysis


def _load_golden():
    try:
        from examples.golden_project.assumptions import golden_assumptions

        return golden_assumptions
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
        return mod.golden_assumptions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=False)
    parser.add_argument("--variable", default="selling_price")
    args = parser.parse_args()
    golden_assumptions = _load_golden()
    base_ass = golden_assumptions()
    runner = ModelRunner(base_ass)
    sens = runner.sensitivity(args.variable, [-10, 0, 10])
    for s in sens:
        result = s["result"]
        irr = f"{result.equity_irr:.2%}" if result.equity_irr else "N/A"
        print(f"{args.variable} {s['change']:+.0f}% -> GDV {result.gdv:,.0f} IRR {irr}")
    print(
        run_sensitivity_analysis(
            {"selling_price": 100}, args.variable, [-10, 0, 10]
        )
    )


if __name__ == "__main__":
    main()
