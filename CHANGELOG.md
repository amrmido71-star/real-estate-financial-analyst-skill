# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
