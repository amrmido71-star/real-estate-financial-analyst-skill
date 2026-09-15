# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-09-15

### Added — Integrated Real Estate Development Model (V1.2 Central Orchestrator)
- **Standard Data Model:** `skill/tools/models/assumptions.py` — `ProjectAssumptions` (Land/Product/Sales/Collection/Construction/Cost/Financing) with `validate()`, `assumption_hash()` for audit trail, datetime-based timelines
- **Central Orchestrator:** `skill/tools/integrated_model.py` — `IntegratedRealEstateModel` implements monthly time engine (36-month default), waterfall `Assumption → Revenue → Collections → Costs → Financing → Cash Flow → Profit → IRR/NPV/Peak`, unit-level inventory (300 units golden), S-Curve construction, LTC-based financing (capitalized vs cash interest), levered/unlevered/equity cash flows, IRR/NPV/MIRR/MOIC/Payback, reconciliation checks, health scoring, dashboard, run_id+timestamp+hash audit trail
- **Model Runner:** `skill/tools/model_runner.py` — `ModelRunner` orchestrates base/best/worst/stress scenarios with true cascade rebuild, one-way & two-way sensitivity matrices, tornado helper
- **Validation & Reporting:** `model_validation.py` (cash/debt/GDV reconciliation, `validate_reconciliation`, `audit_trail`) + `reporting.py` (`build_dashboard`, `build_executive_summary`, `build_management_pack` — decision Recommended/Watch/Not Recommended linked to hurdle 18%)
- **8 Engines Layer:** `skill/tools/engines/` — `revenue_engine`, `sales_engine`, `collection_engine`, `construction_engine`, `financing_engine`, `cashflow_engine`, `return_engine` (IRR/NPV/MOIC/DSCR/WACC/Break-even/Valuation), `scenario_engine` (Monte Carlo optional, tornado, two-way)
- **Models Package Refactor:** `skill/tools/base_models.py` (legacy Unit/CostItem/Sale/Collection/Project preserved for backward compat) + `skill/tools/models/__init__.py` re-exports + 8 typed aliases `project/unit/sales/collections/construction/financing/cashflow/valuation`
- **Golden Project:** `examples/golden_project/` — flagship East Cairo Compound (300 units, 85k sqm sellable @34k EGP, 1.05B construction, 420M land) — `assumptions.py` + `run.py` (full pipeline demo) + `expected_metrics.json` + `README.md`; audited band GDV 2.83B / GDC 1.85B / Profit 985M / 34.8% margin / 30.4% equity IRR / 122M NPV @14% / 1.97 MOIC / Healthy 100; stress scenarios rebuild end-to-end
- **Tests:** `tests/test_integrated_model.py` — 12 new tests (golden reconciliation, returns sanity, peak equity/debt, scenario cascade, sensitivity monotonic, two-way shape, delay impact, debt LTC sanity, inventory, escalation, monthly engine, hash stability) — total 166 passing
- **Investor Metrics Fix:** overflow-safe `_npv_at` / `_npv_derivative` for large cash flows (billions) monthly IRR
- **Financing Fix:** capitalized interest + debt repayment from surplus, equity injection/distribution split, peak funding via levered cumulative minimum (not net-zero after equity)
- **Infra:** pyproject 1.2.0, exports wired in `skill/tools/__init__.py`, ruff fixes, engines wrapping legacy modules

### Changed
- `skill/tools/models.py` → `skill/tools/base_models.py` + `skill/tools/models/` package with backward-compat `base_models` alias — no breaking import change (still `from skill.tools.base_models import Unit`)
- `skill/tools/investment_metrics.py` hardened for billion-scale monthly cash flows

### Fixed
- Peak funding previously 0 (net after equity injection) — now correctly peak funding = |min levered cumulative| (305M base)
- Equity IRR previously inflated due to missing debt repayment — now correctly 30.4% base (vs 104% before)
- Golden project previously empty — now audited flagship

## [1.1.0] - 2026-09-14

### Added
- **New Engines (8):**
  - `sales_collection.py` — unit inventory, installment schedules, monthly cash aggregation, aging buckets (0-30/180+), velocity, collection metrics
  - `construction_analysis.py` — EAC/ETC, variance, S-Curve (standard/front/back/linear), monthly progress reports
  - `financing.py` — LTC/LTV, drawdown/repayment schedule, capitalized interest, DSCR series, facility headroom, levered vs unlevered
  - `financial_statements.py` — Income Statement, Balance Sheet, Cash Flow + 13 ratios (Current, Quick, D/E, Interest Coverage, AR/AP Days, CCC, ROE/ROA)
  - `portfolio_analysis.py` — multi-project aggregation, weighted margin, portfolio IRR/NPV, ranking, concentration risk
  - `valuation.py` — WACC (CAPM), DCF with terminal value (Gordon & Exit Cap), Residual Land Value, Comparable, Income/NOI
  - `data_loader.py` — unified CSV/Excel ingestion, column normalization, schema validation
  - `models.py` — typed dataclasses (Project, Unit, CostItem, Sale, Collection, CashFlowPeriod, FinancialStatement)
  - `exceptions.py` — domain exceptions (InvalidDiscountRate, MissingRequiredField, MultipleIRR, etc.)

- **Enhanced Engines:**
  - `investment_metrics.py` — unified NPV (Period 0 not discounted), `calculate_npv_with_initial`, MIRR, `detect_multiple_irr`, `count_sign_changes`, `irr_with_diagnostics`
  - `project_metrics.py` — unified break-even: `calculate_break_even_revenue` = Cost/(1-TargetMargin), `calculate_break_even_price` = Revenue/Area, `calculate_break_even_units`, `calculate_safety_margin`
  - `cashflow_analysis.py` — `build_detailed_cashflow` with CashFlowPeriod, period types (monthly/quarterly/annual), `aggregate_to_quarterly/annual`, funding gap
  - `scenario_analysis.py` — true financial rebuild: Assumption → Revenue → Collection → Cost → Cash Flow → IRR/NPV/Peak Funding; 10+ assumption types, two-way sensitivity matrix, tornado ranking
  - `data_validation.py` — datetime parsing (not string compare), type/numeric validation, 12 business rules, `validate_transactions`, `calculate_data_quality_score` (0-100), `assess_confidence` (High/Med/Low)

- **Testing:**
  - Added 7 new test suites: `test_data_validation.py`, `test_sales_collection.py`, `test_construction_analysis.py`, `test_financing.py`, `test_financial_statements.py`, `test_valuation.py`, `test_portfolio.py`, `test_investment_mirr.py`, `test_scenario_sensitivity_new.py`, `test_integration.py`
  - Total: 154 tests passing (from 54 in v1.0.0)
  - Integration test: full project mock (Land + Construction + Sales + Financing + Scenario)
  - Regression tests: NPV period-zero, break-even formula, sensitivity rebuild

- **Infrastructure:**
  - `pyproject.toml` updated: version 1.1.0, correct repo URLs (amrmido71-star), Development Status Beta, added ruff/mypy to dev
  - `.github/workflows/tests.yml` — CI for Python 3.9-3.12 (pytest + ruff + mypy)
  - `skill/tools/__init__.py` — unified exports with version 1.1.0

### Fixed
- **NPV:** unified convention `cash_flows[0]=Period 0` not discounted; separated `calculate_npv_with_initial`; added validation for rate <= -1
- **Break-even:** unified definition `Revenue = Cost/(1-TargetMargin)`, Price = Revenue/Area, consistent across code/docs/tests
- **Scenario Engine:** now rebuilds dependent cash flows instead of scaling KPIs directly; supports 10 variables and two-way matrices
- **README:** replaced placeholder URLs (`your-org`) with `amrmido71-star`
- **PDF Support:** clarified as Roadmap (not claimed as implemented) in README/docs

### Changed
- `pyproject.toml` Development Status: `Production/Stable` → `Beta` (more honest until v1.1 validated in production)
- `data_validation` now uses `datetime.strptime` parsing, not string comparison

## [1.0.0] - 2026-09-14

### Added
- Initial production release
- Core financial calculation engine (`financial_calculations.py`)
- Real estate project metrics engine (`project_metrics.py`)
- Cash flow analysis engine (`cashflow_analysis.py`)
- Investment metrics & valuation engine (`investment_metrics.py`)
- Scenario & sensitivity analysis engine (`scenario_analysis.py`)
- Data validation engine (`data_validation.py`)
- 6 professional workflows (Monthly, Project, Budget vs Actual, Cashflow Forecast, Investment, Management Reporting)
- 5 prompt templates (System, Financial, Project, Cashflow, Variance, Investment)
- 6 knowledge bases (Real Estate Finance, Metrics, Valuation, Cashflow, Rules)
- 3 financial rules configs (settings, financial_rules, industry_benchmarks)
- 5 report templates (Executive Summary, Financial Analysis, Project Analysis, Variance, Investment Memo)
- 3 mock examples (Project, Financials CSV, Cashflow CSV, Full Analysis)
- Comprehensive test suite (5 test modules, 70+ tests)
- Full Arabic & English documentation (README, GETTING_STARTED, USAGE, METRICS, WORKFLOWS, TROUBLESHOOTING)
- GitHub-ready structure (LICENSE, CONTRIBUTING, .gitignore, pyproject.toml)

### Documentation
- README.md (English) and README_AR.md (Arabic)
- docs/GETTING_STARTED_AR.md, USAGE_AR.md, FINANCIAL_METRICS_AR.md, WORKFLOWS_AR.md, TROUBLESHOOTING_AR.md

## [Unreleased]
- PDF financial statement parser (planned — see Roadmap)
- Interactive dashboard generator (HTML)
- IFRS 15 Revenue Recognition automation
- Multi-currency FX handling
