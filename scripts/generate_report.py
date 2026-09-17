#!/usr/bin/env python3
"""Wrapper: python scripts/generate_report.py --result out/kpis.json --template templates/executive-report.md"""

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skill"))

from tools.integrated_model import IntegratedRealEstateModel
from tools.reporting import build_executive_summary


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
    parser.add_argument("--result", required=False)
    parser.add_argument("--template", default="templates/executive-report.md")
    args = parser.parse_args()
    _ = args  # parsed for future use; report currently uses golden assumptions
    golden_assumptions = _load_golden()
    ass = golden_assumptions()
    result = IntegratedRealEstateModel(ass).run()
    print(build_executive_summary(result)[:2000])


if __name__ == "__main__":
    main()
