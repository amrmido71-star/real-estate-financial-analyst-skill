# Workflow — Project Financial Analysis (Feasibility)

**Purpose:** Full feasibility & profitability analysis for a single development project.
**When:** New project evaluation, quarterly reforecast, investment committee
**Inputs:** Land, Costs, Unit Mix, Areas, Prices, Schedules, Financing

## Steps

### 1. Project Definition (10 min)
- Project name, location, type (residential/commercial/mixed), scale, timeline, currency
- Confirm scope: sell-out vs rental hold

### 2. Data Intake (20 min)
| Input Group | Required Fields |
|-------------|-----------------|
| Land | Cost, area, acquisition date |
| Construction | Hard cost total or per SQM, phasing |
| Infra/Soft | Design, consultancy, PM |
| S&M | Marketing, commission %, admin |
| Financing | Debt %, rate, fees |
| Contingency | % or amount |
| Unit Mix | Type, units, area, price/unit, price/SQM |
| Schedules | Sales velocity, collection plan, construction S-curve |

- Run validation: land/cost negative?, area logic, GDV/GDC sum checks
- Use prompt: `project_analysis_prompt.md`

### 3. Revenue (GDV) Build (15 min)
- Calculate GDV per unit type and total (project_metrics.calculate_gdv)
- Price/SQM per type, weighted average
- Compare to comps — flag if >15% above/below market

### 4. Cost (GDC) Build (15 min)
- Sum all cost items → GDC (project_metrics.calculate_gdc)
- Ratios: Land%, Construction%, S&M%, Financing%
- Cost/SQM (BUA and sellable)
- Compare to benchmarks — flag overruns

### 5. Profitability (10 min)
- Gross Profit = GDV − GDC
- Development Margin, Margin on Cost, Profit/SQM
- Benchmark verdict

### 6. Investment Metrics (20 min)
- Build timeline cash flows (monthly) from schedules
- Calculate: Project IRR, NPV, Equity IRR, Equity Multiple, Payback
- Compare to hurdle (settings.yaml: 18%)
- Use: `investment_metrics.py`

### 7. Break-even (10 min)
- Break-even Sales Value & %, Break-even Price, Safety Margin
- Interpret: How far can price/sales fall before loss?

### 8. Scenarios (15 min)
- Define assumptions table for Base / Best / Worst
  - Best: Price +5-10%, Cost −5-10%, Faster sales, Better collection
  - Worst: Price −10%, Cost +15%, Slower sales, Collection delays, Rate +2%
- Re-run model for each → comparison table
- Use: `scenario_analysis.py`

### 9. Sensitivity (15 min)
- Vary one variable at a time: Price ±10%, Cost ±15%, Delay ±6mo, Rate ±2%
- Tornado ranking — identify #1 driver
- Use: `scenario_analysis.run_sensitivity_analysis`

### 10. Risk Assessment (10 min)
- Score 10 risks (Probability × Impact)
- Early Warning Indicators
- Mitigations

### 11. Executive Summary & Recommendation (15 min)
- Health, GDV/GDC/Margin/IRR/NPV, Peak Funding, Break-even
- Go / No-Go / Conditional with price/cost/velocity conditions
- Use template: `templates/project_analysis_report.md` + `templates/investment_memo.md`

## Deliverables
- [ ] Feasibility Report (10-15 pages)
- [ ] Investment Memo (2 pages)
- [ ] Scenario & Sensitivity Tables
- [ ] Cash Flow Forecast & Peak Funding Chart Narrative

## Decision Gate
- If Development Margin <15% or IRR < hurdle, require mitigation plan before approval.
- If Break-even >70%, flag high risk.
