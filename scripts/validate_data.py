#!/usr/bin/env python3
"""Wrapper: python scripts/validate_data.py --input data.json"""

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "skill"))

from tools.data_validation import (
    calculate_data_quality_score,
    validate_financials,
    validate_project,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    data = json.loads(pathlib.Path(args.input).read_text())
    if "total_units" in str(data):
        res = validate_project(data)
    else:
        res = validate_financials(data)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print("score", calculate_data_quality_score(res))


if __name__ == "__main__":
    main()
