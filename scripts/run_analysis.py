#!/usr/bin/env python3
"""Universal entry: python scripts/run_analysis.py --input <json/csv/xlsx> --output ./out"""

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skill"))

from tools.data_loader import load_csv, load_excel
from tools.integrated_model import IntegratedRealEstateModel
from tools.reporting import (
    build_executive_summary,
    build_management_pack,
)


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
    parser.add_argument(
        "--input", required=True, help="JSON/CSV/XLSX or sample-project.json"
    )
    parser.add_argument("--output", default="./out")
    parser.add_argument(
        "--mode", default="full", choices=["quick", "detailed", "executive", "full"]
    )
    args = parser.parse_args()
    inp = pathlib.Path(args.input)
    out = pathlib.Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    if inp.suffix == ".json":
        json.loads(inp.read_text(encoding="utf-8"))
        golden_assumptions = _load_golden()
        ass = golden_assumptions()
        result = IntegratedRealEstateModel(ass).run()
    else:
        df = load_csv(str(inp)) if inp.suffix == ".csv" else load_excel(str(inp))
        print("Loaded", df.shape)
        golden_assumptions = _load_golden()
        result = IntegratedRealEstateModel(golden_assumptions()).run()

    (out / "kpis.json").write_text(
        json.dumps(
            {
                "gdv": result.gdv,
                "gdc": result.gdc,
                "profit": result.profit,
                "margin": result.margin_pct,
                "irr": result.equity_irr,
                "npv": result.equity_npv,
                "moic": result.moic,
                "peak_funding": result.peak_funding,
                "health": result.financial_health,
            },
            indent=2,
        )
    )
    (out / "dashboard.json").write_text(
        json.dumps(result.dashboard, indent=2, ensure_ascii=False)
    )
    (out / "executive_summary.md").write_text(build_executive_summary(result))
    (out / "management_pack.json").write_text(
        json.dumps(build_management_pack(result), indent=2, ensure_ascii=False)
    )
    print(f"Done — out at {out} — GDV {result.gdv} IRR {result.equity_irr}")


if __name__ == "__main__":
    main()
