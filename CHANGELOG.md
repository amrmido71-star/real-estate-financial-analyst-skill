# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Excel ingestion helpers
- PDF financial statement parser
- Interactive dashboard generator
- IFRS 15 Revenue Recognition automation
