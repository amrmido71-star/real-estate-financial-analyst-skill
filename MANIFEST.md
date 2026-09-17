# Package Manifest — Real Estate Financial Analyst V1.2.2

## Package

- **Name:** real-estate-financial-analyst
- **Version:** 1.2.2
- **Format:** Portable AI Skill (Agent Skills compatible)
- **Package Directory:** `real-estate-financial-analyst-v1.2.2/`
- **Archives:** `real-estate-financial-analyst-v1.2.2.zip` / `.tar.gz` (identical contents)
- **License:** MIT

## Files Included

- `COMPATIBILITY.md`
- `LICENSE`
- `README.md`
- `SKILL.md`
- `examples/golden_project/README.md`
- `examples/golden_project/assumptions.py`
- `examples/golden_project/expected_metrics.json`
- `examples/golden_project/run.py`
- `examples/sample-executive-report.md`
- `examples/sample-project-analysis.md`
- `examples/sample-project.json`
- `examples/sample-scenario-analysis.md`
- `references/cash-flow.md`
- `references/construction-costs.md`
- `references/financial-modeling.md`
- `references/financing.md`
- `references/forecasting.md`
- `references/irr-npv-mirr-moic.md`
- `references/management-reporting.md`
- `references/profitability.md`
- `references/real-estate-modeling.md`
- `references/risk-analysis.md`
- `references/sales-collection.md`
- `references/scenario-analysis.md`
- `references/sensitivity-analysis.md`
- `references/valuation.md`
- `requirements.txt`
- `pyproject.toml`
- `docs/INTEGRATED_MODEL.md`
- `docs/FINAL_REPORT_V1_2_2.md`
- `scripts/generate_report.py`
- `scripts/run_analysis.py`
- `scripts/run_scenarios.py`
- `scripts/run_sensitivity.py`
- `scripts/validate_data.py`
- `skill/tools/__init__.py`
- `skill/tools/base_models.py`
- `skill/tools/cashflow_analysis.py`
- `skill/tools/construction_analysis.py`
- `skill/tools/data_loader.py`
- `skill/tools/data_validation.py`
- `skill/tools/engines/__init__.py`
- `skill/tools/engines/cashflow_engine.py`
- `skill/tools/engines/collection_engine.py`
- `skill/tools/engines/construction_engine.py`
- `skill/tools/engines/financing_engine.py`
- `skill/tools/engines/return_engine.py`
- `skill/tools/engines/revenue_engine.py`
- `skill/tools/engines/sales_engine.py`
- `skill/tools/engines/scenario_engine.py`
- `skill/tools/exceptions.py`
- `skill/tools/financial_calculations.py`
- `skill/tools/financial_statements.py`
- `skill/tools/financing.py`
- `skill/tools/integrated_model.py`
- `skill/tools/investment_metrics.py`
- `skill/tools/model_runner.py`
- `skill/tools/model_validation.py`
- `skill/tools/models/__init__.py`
- `skill/tools/models/assumptions.py`
- `skill/tools/models/cashflow.py`
- `skill/tools/models/collections.py`
- `skill/tools/models/construction.py`
- `skill/tools/models/financing.py`
- `skill/tools/models/project.py`
- `skill/tools/models/sales.py`
- `skill/tools/models/unit.py`
- `skill/tools/models/valuation.py`
- `skill/tools/portfolio_analysis.py`
- `skill/tools/project_metrics.py`
- `skill/tools/reporting.py`
- `skill/tools/sales_collection.py`
- `skill/tools/scenario_analysis.py`
- `skill/tools/valuation.py`
- `templates/cash-flow-report.md`
- `templates/collection-report.md`
- `templates/executive-report.md`
- `templates/financing-report.md`
- `templates/forecast-report.md`
- `templates/monthly-financial-report.md`
- `templates/profitability-report.md`
- `templates/project-feasibility-report.md`
- `templates/risk-report.md`
- `templates/sales-report.md`
- `templates/scenario-report.md`
- `templates/sensitivity-report.md`
- `tests/__init__.py`
- `tests/test_cashflow.py`
- `tests/test_construction_analysis.py`
- `tests/test_data_validation.py`
- `tests/test_financial_calculations.py`
- `tests/test_financial_statements.py`
- `tests/test_financing.py`
- `tests/test_hardening_v1_2_1.py`
- `tests/test_integrated_model.py`
- `tests/test_integration.py`
- `tests/test_investment_metrics.py`
- `tests/test_investment_mirr.py`
- `tests/test_portfolio.py`
- `tests/test_project_metrics.py`
- `tests/test_sales_collection.py`
- `tests/test_scenario_sensitivity_new.py`
- `tests/test_scenarios.py`
- `tests/test_valuation.py`

## Runtime Requirements

- Python ≥3.9
- Dependencies: `pip install -r requirements.txt`
  - pyyaml>=6.0
  - pandas>=1.5.0
  - numpy>=1.23.0
  - openpyxl>=3.1.0
  - (dev) pytest>=7.0, pytest-cov, ruff, mypy

## Entry Points

| Entry | Command | Input | Output |
|-------|---------|-------|--------|
| Universal | `python scripts/run_analysis.py --input <file> --output ./out` | JSON/CSV/XLSX (`examples/sample-project.json`) | `out/kpis.json`, `dashboard.json`, `executive_summary.md`, `management_pack.json` |
| Validate | `python scripts/validate_data.py --input <file>` | JSON | console validation + score |
| Scenarios | `python scripts/run_scenarios.py` | (uses golden_project assumptions) | console: base/best/worst |
| Sensitivity | `python scripts/run_sensitivity.py --variable selling_price` | variable name | console: -10%/+10% GDV/IRR |
| Report | `python scripts/generate_report.py --result out/kpis.json` | kpis.json | executive summary preview |
| Golden | `python examples/golden_project/run.py` | (internal assumptions) | dashboard + reconciliation |
| Tests | `pytest -q` | — | 202 tests |

## Expected Input

- **JSON:** `ProjectAssumptions` schema — see `examples/sample-project.json` and `skill/tools/models/assumptions.py`
- **CSV/XLSX:** Sales/collections/construction via `skill/tools/data_loader.py` (READ-ONLY)
- See `references/data-validation.md` and `references/financial-modeling.md`

## Expected Outputs

- **SKILL.md discovery:** Agent loads skill when prompt matches financial analysis intents (see SKILL.md When to Use)
- **kpis.json:** `gdv`, `gdc`, `profit`, `margin_pct`, `equity_irr`, `equity_npv`, `moic`, `peak_funding`, `health`
- **Golden metrics (East Cairo Compound 300 units):**
  - GDV = 2,832,200,000
  - GDC = 1,846,558,233
  - Profit = 985,641,767
  - Margin = 34.8%
  - Equity IRR = 30.4% (levered); Unlevered IRR = 21.25%
  - NPV = 122,599,192 (discount 14%)
  - MOIC = 1.97
  - Peak Funding = 305,865,252 (Peak Debt 835,881,180)
  - Health = Healthy (100/100), reconciliation PASS

## Supported Installation Models

- **Method A — Agent Skills:** Upload/install skill package, enable skill. Done. — For agents supporting Agent Skills format.
- **Method B — Generic Agent:** Copy directory into agent's skills directory, `pip install -r requirements.txt`, run `scripts/*`.
- **Method C — Manual / No-Skills:** Provide `SKILL.md` + `references/` + `templates/` as instructions; optionally execute bundled Python scripts.

All via: "Works with agents that support the Agent Skills format, or agents that can load SKILL.md and access the bundled resources/scripts."

## Progressive Disclosure

`SKILL.md` = router (identity, when to use, workflow, engine references). Details in `references/` (14 docs), `templates/` (12), `examples/` (4), `skill/tools/` (engine). No duplication: ONE engine (`skill/tools/integrated_model.py` + `engines/*`), wrappers call same engine.

## Security

- No secrets, tokens, API keys, passwords in package (verified via scan for `ghp_`, `github_pat_`, `token`, `secret`, `password`, `api_key`).
- Source data READ-ONLY; outputs separate files.

## Distribution

```
distribution/
├── real-estate-financial-analyst-v1.2.2.zip
├── real-estate-financial-analyst-v1.2.2.tar.gz
├── SHA256SUMS
└── MANIFEST.md  (this file)
```

No `__pycache__`, `.pytest_cache`, `.git`, `.coverage`, `.mypy_cache`, `dist`, `build`, temporary files.

