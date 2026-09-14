# Real Estate Financial Analyst Skill

> **Professional, production-ready AI Skill that turns any AI Agent into a Senior Real Estate Development Financial Analyst (FP&A + Investment Analysis + Development Feasibility).**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-154%20passing-brightgreen)](#testing)
[![Version](https://img.shields.io/badge/Version-1.1.0-orange)](#)

**Bilingual:** English + Arabic — responds in user's language.  
**Domain:** Residential, Commercial, Mixed-Use, Hospitality, Land Development — adaptable to any market (MENA, GCC, Global).  
**Agent-Agnostic:** Works with Claude, GPT, Gemini, or any LLM via System Prompt injection.

---

## ✨ What It Does

| Capability | Description |
|------------|-------------|
| **Financial Statement Analysis** | P&L, BS, Cash Flow — vertical/horizontal, margins, EBITDA, Net |
| **Project Feasibility** | GDV, GDC, Development Margin, Profit/SQM, Cost Ratios, Residual Land Value |
| **Sales & Collections** | Sold vs Available, Sales Rate, ASP, Collection Efficiency, Aging |
| **Cash Flow & Liquidity** | Operating / Development / Financing flows, Cumulative, Peak Funding, Runway, DSCR |
| **Budget vs Actual** | Absolute & % variance, Favorable/Unfavorable/Neutral, driver analysis |
| **Investment Metrics** | IRR, NPV, ROI, ROIC, Equity Multiple, Cash-on-Cash, Payback |
| **Scenarios** | Base / Best / Worst comparison table |
| **Sensitivity** | Price, Cost, Velocity, Rate, Delay — Tornado ranking |
| **Risk Framework** | 10 risk categories with Prob×Impact, Early Warning Indicators |
| **Executive Reporting** | Board-ready Executive Summary + Detailed Reports + Variance & Investment Memos |

**Principle:** The analyst thinks like a **CFO advisor, not a calculator** — every number gets a driver, risk, and recommendation. **Never fabricates data.**

---

## 🆕 What's New in v1.1.0 (2026-09-14)

**Major upgrade from v1.0.0 → v1.1.0: 154 tests passing (from 54)**

| Area | Improvement |
|------|-------------|
| **NPV Engine** | Unified `Period 0 not discounted`, `calculate_npv_with_initial`, validated `rate > -1` |
| **Break-even** | Unified `Revenue = Cost/(1-TargetMargin)`, `Price = Revenue/Area`, 0%/10%/20%/50% tests |
| **Scenario Engine** | True rebuild: Assumption → Revenue → Collections → Cost → Financing → Cash Flow → IRR/NPV/Peak. Supports 10 variables + two-way matrix |
| **Sensitivity** | One-way + Two-way matrices + Tornado ranking, all rebuild cash flows |
| **MIRR / Multiple IRR** | `calculate_mirr`, `detect_multiple_irr`, `count_sign_changes`, `irr_with_diagnostics` |
| **8 New Engines** | `sales_collection`, `construction_analysis` (EAC/S-Curve), `financing` (LTC/LTV/DSCR), `financial_statements` (13 ratios), `portfolio_analysis`, `valuation` (WACC/DCF/Residual/Comparable/Income), `data_loader` (CSV/Excel), `models` (dataclasses) |
| **Data Validation** | `datetime` parsing, 12 business rules, `calculate_data_quality_score` (0-100), `assess_confidence` |
| **CI/CD** | `.github/workflows/tests.yml` for Python 3.9-3.12 (pytest+ruff+mypy) |
| **Docs** | All placeholders fixed (`amrmido71-star`), PDF clarified as Roadmap |

See `CHANGELOG.md` for full details.

---

## 📁 Project Structure

```
real-estate-financial-analyst-skill/
├── README.md / README_AR.md
├── LICENSE / CHANGELOG.md / CONTRIBUTING.md
├── requirements.txt / pyproject.toml / .gitignore
│
├── skill/
│   ├── SKILL.md                          # ★ Core skill definition (Role, Responsibilities, Engine)
│   ├── config/
│   │   ├── settings.yaml                 # Company defaults (currency, hurdle, thresholds)
│   │   ├── financial_rules.yaml          # Validation & calculation rules
│   │   └── industry_benchmarks.yaml      # Benchmarks by segment (residential/commercial/etc.)
│   ├── prompts/
│   │   ├── system_prompt.md              # Main system prompt for agent injection
│   │   ├── financial_analysis_prompt.md
│   │   ├── project_analysis_prompt.md
│   │   ├── cashflow_analysis_prompt.md
│   │   ├── variance_analysis_prompt.md
│   │   └── investment_analysis_prompt.md
│   ├── knowledge/
│   │   ├── real_estate_finance.md
│   │   ├── financial_metrics.md
│   │   ├── real_estate_metrics.md
│   │   ├── valuation_methods.md
│   │   ├── cashflow_methods.md
│   │   └── financial_analysis_rules.md
│   ├── workflows/
│   │   ├── monthly_financial_analysis.md
│   │   ├── project_financial_analysis.md
│   │   ├── budget_vs_actual.md
│   │   ├── cashflow_forecast.md
│   │   ├── investment_analysis.md
│   │   └── management_reporting.md
│   ├── templates/
│   │   ├── executive_summary.md
│   │   ├── financial_analysis_report.md
│   │   ├── project_analysis_report.md
│   │   ├── variance_report.md
│   │   └── investment_memo.md
│   └── tools/ (Python engine — 14 modules)
│       ├── financial_calculations.py     # Gross Profit/Margin, EBITDA, Variance, Break-even, ROI
│       ├── project_metrics.py            # GDV, GDC, Margin, per SQM, Break-even (unified)
│       ├── cashflow_analysis.py          # Detailed periods, Peak Funding, DSCR, quarterly/annual
│       ├── investment_metrics.py         # IRR, NPV (Period 0), MIRR, Multiple IRR detection
│       ├── scenario_analysis.py          # True rebuild, Two-way, Tornado
│       ├── data_validation.py            # datetime, Quality Score, Confidence
│       ├── sales_collection.py           # Installments, Aging buckets, Velocity
│       ├── construction_analysis.py      # EAC/ETC, S-Curve, Progress report
│       ├── financing.py                  # LTC/LTV, Drawdown, DSCR, Headroom
│       ├── financial_statements.py       # IS/BS/CF + 13 ratios
│       ├── portfolio_analysis.py         # Multi-project, ranking, concentration
│       ├── valuation.py                  # WACC/CAPM, DCF, Residual, Comparable, Income
│       ├── data_loader.py                # CSV/Excel, column normalization
│       ├── models.py                     # Dataclasses (Project, Unit, Sale...)
│       └── exceptions.py                 # Domain exceptions
│
├── examples/
│   ├── example_project.md                # Mock project: 500 units, 62k SQM, 1.75B GDV
│   ├── example_financials.csv            # 6 quarters P&L + Budget
│   ├── example_cashflow.csv              # 15-month forecast
│   └── example_analysis.md               # Full sample output (Executive Summary + Details)
│
├── tests/ (154 tests)
│   ├── test_financial_calculations.py
│   ├── test_project_metrics.py
│   ├── test_cashflow.py
│   ├── test_investment_metrics.py
│   ├── test_investment_mirr.py          # MIRR & multiple IRR
│   ├── test_scenarios.py
│   ├── test_scenario_sensitivity_new.py # True rebuild + two-way
│   ├── test_data_validation.py
│   ├── test_sales_collection.py
│   ├── test_construction_analysis.py
│   ├── test_financing.py
│   ├── test_financial_statements.py
│   ├── test_valuation.py
│   ├── test_portfolio.py
│   └── test_integration.py              # Full mock project
│
├── .github/workflows/tests.yml           # CI (3.9-3.12)
│
└── docs/
    ├── GETTING_STARTED_AR.md             # Arabic quick start
    ├── USAGE_AR.md                       # Full usage guide (AR)
    ├── FINANCIAL_METRICS_AR.md           # Every metric explained (AR)
    ├── WORKFLOWS_AR.md                   # All 6 workflows (AR)
    └── TROUBLESHOOTING_AR.md             # Troubleshooting (AR)
```

---

## 🚀 Quick Start

### 1. Install

```bash
git clone https://github.com/amrmido71-star/real-estate-financial-analyst-skill.git
cd real-estate-financial-analyst-skill
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v  # should pass 154 tests
```

### 2. Use in Python (no agent needed)

```python
from skill.tools.financial_calculations import calculate_gross_margin, calculate_variance, classify_variance
from skill.tools.project_metrics import calculate_gdv, calculate_gdc, calculate_development_margin
from skill.tools.investment_metrics import calculate_irr, calculate_npv

# Gross Margin
print(calculate_gross_margin(1_000_000, 650_000))  # 35.0%

# Project
gdv = calculate_gdv([{"units": 100, "price_per_unit": 2_000_000}])
gdc = calculate_gdc({"land": 40_000_000, "construction": 90_000_000, "soft": 15_000_000})
print(f"Development Margin: {calculate_development_margin(gdv, gdc):.1f}%")

# Investment
cfs = [-100_000_000, 30_000_000, 50_000_000, 70_000_000]
print(f"IRR: {calculate_irr(cfs)*100:.1f}%")
print(f"NPV @15%: {calculate_npv(cfs, 0.15):,.0f}")

# Variance
print(calculate_variance(112_000_000, 100_000_000))  # 12,000,000
print(classify_variance(112_000_000, 100_000_000, is_revenue=False))  # Unfavorable
```

### 3. Use with an AI Agent

**Option A — System Prompt Injection (simplest):**
1. Copy `skill/prompts/system_prompt.md` as the agent's System Prompt.
2. Upload `skill/knowledge/*.md` as knowledge base.
3. Register `skill/tools/*.py` as function tools (if supported).
4. Ask: *"Analyze this project: Land 50M, Construction 120M, Sellable 10k SQM, Price 25k/SQM"*

**Option B — Reference SKILL.md:**
Point the agent to `skill/SKILL.md` at startup — it contains the full role definition.

**Option C — Python Import:**
Import tools directly as above in any Python-capable agent.

Edit `skill/config/settings.yaml` for your company (currency, VAT, hurdle rate 18%, thresholds).

---

## 📊 Example Output (Executive Summary)

```
OVERALL HEALTH: Watchlist
Stable margin 32% but liquidity tightening — runway 2.8 months, collection 86%

KEY FINDINGS:
1. Gross Margin 32% vs 35% budget (−3pts) — construction +11.5% overrun
2. Net Margin 10.9% vs 13.3% budget — below benchmark 18%
3. Sales 65 vs 70 units (−7.1%) — velocity 5% behind plan

PROJECT: Green Valley — GDV 1.75B | GDC 1.25B | Margin 28.6% | IRR 18.2% | NPV +58M | Break-even 71.4%

CASH FLOW: Peak Funding −77.9M at M9 | Recovery M14 | DSCR ~1.0 trough (warning <1.2)
COLLECTIONS: Efficiency 86.1% vs 88% target — 9.4M overdue

TOP RISKS:
1. Liquidity — Critical — accelerate 91-180d collections (22M)
2. Cost Overrun — High — renegotiate steel bulk
3. Sales Velocity — Medium — promo on 2BR

RECOMMENDATIONS:
1. Weekly collection sprint (Owner: Collection Mgr, 60 days, +8M cash)
2. Review BOQ & raise contingency 5%→7% (Owner: PM, 14 days)
3. Confirm facility +20M headroom (Owner: CFO, 14 days)
```

Full example: `examples/example_analysis.md`

---

## 🧮 Metrics Engine

| Group | Metrics |
|-------|---------|
| **Profitability** | Revenue, COR, Gross Profit/Margin, Operating Profit, EBITDA/EBIT, Net Profit/Margin |
| **Investment** | ROI, IRR, NPV, ROIC, Equity Multiple, Cash-on-Cash, Payback |
| **Real Estate** | GDV, GDC, Development Margin, Profit/SQM, Cost/SQM, Price/SQM, Land%, Construction%, Residual Land Value |
| **Sales** | Sales Value, Units Sold/Available, Sales Rate, ASP, Price/SQM, Cancellation Rate |
| **Collections** | Contracted vs Collected vs Outstanding, Efficiency, Aging, Overdue |
| **Cash Flow** | Operating / Development / Financing CF, Free CF, Net, Cumulative, Peak Funding, Runway, DSCR |
| **Variance** | Absolute, %, Favorable/Unfavorable/Neutral, Driver (Volume/Price/Mix/Timing) |

See `docs/FINANCIAL_METRICS_AR.md` for formulas & benchmarks.

---

## 🔄 Workflows

| Workflow | When | Template |
|----------|------|----------|
| Monthly Financial Analysis | Monthly FP&A pack | `financial_analysis_report.md` |
| Project Financial Analysis | New project / quarterly reforecast | `project_analysis_report.md` |
| Budget vs Actual | Monthly variance review | `variance_report.md` |
| Cash Flow Forecast | Liquidity & peak funding | (Cash Flow section) |
| Investment Analysis | IC decision / land bid | `investment_memo.md` |
| Management Reporting | Board / CEO pack | `executive_summary.md` |

Details: `docs/WORKFLOWS_AR.md`

---

## 🧪 Testing

```bash
pytest -v                          # 154 tests
pytest --cov=skill/tools
pytest tests/test_investment_mirr.py -v
```

- **154 tests** covering all 14 engines, edge cases, regression, integration.
- Includes: division by zero, missing data, IRR convergence, MIRR/multiple IRR, scenario rebuild, two-way sensitivity, S-Curve, aging buckets, WACC, portfolio, DCF.
- Guarded against: division by zero, missing inputs, negative revenue, sold>total, date logic (datetime), totals mismatch.

---

## 🌍 Adapt to Your Market

Edit `skill/config/settings.yaml`:

```yaml
company:
  default_currency: "EGP"   # SAR / AED / USD / EUR
  tax_rate: 0.225
thresholds:
  irr_hurdle_rate: 18.0
  variance_neutral_pct: 2.0
```

And `skill/config/industry_benchmarks.yaml` for local benchmarks by segment.

---

## 🧠 How the Agent Thinks (Chain-of-Thought)

```
1. Understand Data → 2. Validate Data → 3. Identify Missing Data
→ 4. Calculate Metrics → 5. Compare (YoY/Budget/Benchmark)
→ 6. Identify Variances → 7. Identify Drivers (Volume/Price/Mix/Timing)
→ 8. Assess Risks → 9. Generate Scenarios → 10. Provide Recommendations
```

If data is missing: *“Data insufficient to calculate [metric] — Required: [X, Y, Z]”* — never fabricates.

---

## 📚 Documentation

| Doc | Language | Content |
|-----|----------|---------|
| `docs/GETTING_STARTED_AR.md` | AR | 10-min quick start |
| `docs/USAGE_AR.md` | AR | Full usage, prompts, examples |
| `docs/FINANCIAL_METRICS_AR.md` | AR | Every metric with formula & benchmark |
| `docs/WORKFLOWS_AR.md` | AR | All 6 workflows |
| `docs/TROUBLESHOOTING_AR.md` | AR | Common issues |
| `README_AR.md` | AR | Arabic README |
| `skill/SKILL.md` | EN | Core skill spec |
| `skill/knowledge/*.md` | EN | Domain knowledge |

---

## 🌐 GitHub Setup

```bash
git init
git add .
git commit -m "feat: initial release — Real Estate Financial Analyst Skill v1.0.0"
git branch -M main
git remote add origin https://github.com/amrmido71-star/real-estate-financial-analyst-skill.git
git push -u origin main
```

Update later:

```bash
git add .
git commit -m "feat: add excel ingestion helpers"
git push
```

See `CONTRIBUTING.md` for contribution guidelines.

---

## 🗺️ Roadmap

- [x] Excel/CSV ingestion helpers (`data_loader.py` — CSV/Excel via pandas/openpyxl)
- [ ] PDF financial statement parser — **planned, not yet implemented** (see `docs/TROUBLESHOOTING_AR.md`)
- [ ] IFRS 15 Revenue Recognition automation
- [ ] Interactive dashboard generator (HTML)
- [ ] Multi-currency FX handling

> **Note on PDF:** README v1.0 claimed PDF support — corrected in v1.1.0. PDF is on Roadmap, not implemented. CSV/Excel is production-ready.

---

## 🤝 Contributing

See `CONTRIBUTING.md`. PRs welcome — please add tests for any formula change.

---

## 📄 License

MIT — see `LICENSE`.

---

## 🙏 Acknowledgments

Crafted for Senior Financial Analysts who refuse to be just calculators.

> **Version 1.1.0 — 2026-09-14 — Production Ready (154 tests passing)**
