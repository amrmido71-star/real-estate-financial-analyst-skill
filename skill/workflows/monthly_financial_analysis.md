# Workflow — Monthly Financial Analysis

**Purpose:** Standard monthly FP&A pack for a Real Estate Development company.
**Frequency:** Monthly
**Owner:** Finance Manager / FP&A
**Inputs:** Trial Balance, Management Accounts (P&L, BS, Cash Flow), Sales & Collection Reports, Budget

## Steps

### 1. Data Intake & Validation (15 min)
- [ ] Import Trial Balance / P&L / BS / Cash Flow (Excel/CSV)
- [ ] Check period, currency, basis (accrual vs cash)
- [ ] Run validation: `data_validation.py` — missing, duplicates, negative revenue, totals
- [ ] Flag gaps — request or label as limitation

### 2. Profitability Analysis (30 min)
- Calculate: Revenue, COR, Gross Profit, Gross Margin, Operating Profit, EBITDA, EBIT, Net Profit, Net Margin
- Vertical analysis (% of revenue) + Horizontal (MoM, YoY, YTD vs Budget)
- Compare to benchmarks (industry_benchmarks.yaml)
- Use prompt: `financial_analysis_prompt.md`

### 3. Sales & Collections (20 min)
- Sales Value, Units Sold/Available, Sales Rate, ASP, Price/SQM
- Contracted vs Recognized vs Collected — efficiency, aging
- Link to P&L revenue — explain gap

### 4. Budget vs Actual (20 min)
- For each P&L line: Absolute + % variance, Favorable/Unfavorable/Neutral
- Rank material variances (>5% or >EGP 500k) — driver analysis (Volume/Price/Mix/Timing)
- Use workflow: `budget_vs_actual.md`

### 5. Cash Flow & Liquidity (20 min)
- Operating, Development, Financing CF, Net, Cumulative
- Peak funding, runway months, collection efficiency
- Compare to forecast — variance commentary
- Use workflow: `cashflow_forecast.md`

### 6. Risk Scan (10 min)
- Run risk framework (10 risks) — score Probability × Impact
- Early Warning Indicators: overdue >20%, margin <15%, DSCR <1.2, inventory months >18

### 7. Executive Summary (15 min)
- Overall Health: Strong/Stable/Watchlist/Weak/Critical
- Key Findings (max 5), Major Risks (3), Recommendations (3-5, actionable)
- Use template: `templates/executive_summary.md`

### 8. Deliverables
- [ ] Executive Summary (1 page)
- [ ] Detailed Financial Analysis Report (`templates/financial_analysis_report.md`)
- [ ] Variance Report (`templates/variance_report.md`)
- [ ] KPI Dashboard Narrative (table + commentary)

### 9. Review & Distribute
- [ ] CFO review
- [ ] Board pack integration
- [ ] Forecast revision trigger if material variance

## Checklist Output
- Health Rating with justification
- Data Quality Findings
- Assumptions & Limitations
- Confidence Level

## Automation Hint
```python
from skill.tools.financial_calculations import calculate_gross_margin, calculate_variance
from skill.tools.cashflow_analysis import analyze_cashflow
from skill.tools.data_validation import validate_financials
```
