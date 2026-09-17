# Real Estate Financial Analyst — Portable AI Skill V1.2.2

Professional Senior Real Estate Financial Analyst skill for development projects — feasibility, profitability (GDV/GDC/Margin/MOIC), cash flow & peak funding, financing (LTC/LTV/DSCR), IRR/NPV/MIRR/MOIC, valuation, forecasting, scenario & sensitivity, risk, and management reporting.

**Version:** 1.2.2 | **Engine:** Integrated Model 90a0d7f | **Tests:** 202 | **Golden:** GDV 2.832B / IRR 30.4% PASS

Portable across AI agents that support Agent Skills or can load SKILL.md and execute the bundled resources/scripts.

---

## QUICK START

1. Download the package.
2. Extract it.
3. Load/install SKILL.md in your AI Agent.
4. Install requirements if Python execution is required.
5. Provide your project data.
6. Ask for the required financial analysis.

**Example prompt:**

> Analyze this real estate project using the Real Estate Financial Analyst skill.

---

## What It Does

- Project feasibility & profitability (GDV/GDC/Profit/Margin/MoC)
- Cash flow, peak funding, DSCR, runway, budget vs actual
- Sales & collections (velocity, aging, efficiency, forecast)
- Construction cost & S-curve, EAC, contingency
- Financing & debt schedule (single source: opening+draw+capInterest-repay=closing)
- Returns: IRR/NPV/MIRR/MOIC/Payback/Break-even (NPV t0 not discounted)
- Valuation: DCF, residual, comparable, WACC
- Scenario (Base/Best/Worst/Stress — full rebuild) & Sensitivity (tornado, one-way/two-way)
- Risk (10 categories, Probability×Impact) & Portfolio
- Management Pack (Executive, Feasibility, Monthly, Risk reports)

---

## Package Contents

```
real-estate-financial-analyst-v1.2.2/
├── SKILL.md
├── README.md
├── COMPATIBILITY.md
├── MANIFEST.md
├── LICENSE
├── requirements.txt
├── SHA256SUMS
├── references/          # 14 progressive disclosure docs
├── templates/           # 12 report templates
├── examples/            # sample-project.json + golden_project (GDV 2.832B)
├── scripts/             # run_analysis, validate_data, run_scenarios, run_sensitivity, generate_report
├── skill/tools/         # Single financial engine (single source of truth)
└── tests/               # 202 tests
```

All calculations via `skill/tools` only. Source data is READ-ONLY.

---

## Installation

### Method A — Agent Skills

1. Upload/install the skill package (`real-estate-financial-analyst-v1.2.2.zip` or `.tar.gz`).
2. Enable the skill (per your agent's Skills mechanism — e.g., import SKILL.md).
3. Done.

Works with agents that support the Agent Skills format, or agents that can load SKILL.md and access the bundled resources/scripts.

### Method B — Generic Agent

1. Copy the skill directory into the agent's skills directory (e.g., `agent/skills/real-estate-financial-analyst-v1.2.2/`).
2. Install requirements if Python execution is needed:
   ```bash
   pip install -r requirements.txt
   ```
3. Run via entry point:
   ```bash
   python scripts/run_analysis.py --input examples/sample-project.json --output ./out
   ```

Works with agents that support the Agent Skills format, or agents that can load SKILL.md and access the bundled resources/scripts.

### Method C — Manual / No-Skills Agent

1. Provide `SKILL.md` + `references/` + `templates/` to the agent (read as instructions).
2. Optionally execute the bundled Python scripts (requires Python ≥3.9 and `pip install -r requirements.txt`):
   ```bash
   python scripts/run_analysis.py --input examples/sample-project.json --output ./out
   python scripts/run_scenarios.py --input project.json
   python scripts/run_sensitivity.py --variable selling_price
   ```

Works with agents that support the Agent Skills format, or agents that can load SKILL.md and access the bundled resources/scripts.

---

## Universal Entry Point

```bash
python scripts/run_analysis.py --input examples/sample-project.json --output ./out
# Other inputs: CSV/Excel via skill/tools/data_loader.py
# Outputs: kpis.json, dashboard.json, executive_summary.md, management_pack.json

python scripts/validate_data.py --input examples/sample-project.json
python scripts/run_scenarios.py
python scripts/run_sensitivity.py --variable selling_price
python scripts/generate_report.py --result out/kpis.json
```

Inputs: JSON / CSV / Excel / dict — see `examples/sample-project.json` and `references/data-validation.md` (and assumptions in `skill/tools/models/assumptions.py`).

---

## Requirements

- Python ≥3.9
- `pip install -r requirements.txt` (pyyaml, pandas, numpy, openpyxl)
- No API keys, tokens, or secrets required — skill is credential-free.

---

## Financial Integrity

- Never fabricate data — missing → `Missing Data | Impact | Required Input`
- Every KPI traceable to source + formula (see `references/`)
- Integrated Model is single source → FinancingEngine → Debt Schedule (reconciliation PASS)
- Scenarios/sensitivity rebuild model — no KPI scaling

---

## Language

Default Arabic (English KPI names in parentheses: العائد الداخلي (Equity IRR)). Switch via prompt: "Respond in English".

---

## Compatibility

See `COMPATIBILITY.md` for platform matrix. Portable across AI agents that support Agent Skills or can load SKILL.md and execute the bundled resources/scripts.

---

## License

MIT — see `LICENSE`
