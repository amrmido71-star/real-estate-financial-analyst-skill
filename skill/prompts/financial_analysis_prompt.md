# Prompt — Financial Statement Analysis (P&L / BS / Cash Flow)

You are performing **Financial Statement Analysis** for a Real Estate Development company.

## Instructions
1. Identify the statement type, period, and currency. If unclear, ask or state assumption.
2. Run data validation (missing, negatives, totals).
3. Calculate:
   - Revenue, COR, Gross Profit, Gross Margin
   - Operating Profit, EBITDA, EBIT, Net Profit, Net Margin
   - YoY and Budget vs Actual if prior/budget data exists
4. Perform vertical analysis (% of revenue) and horizontal analysis (change %).
5. Compare to industry benchmarks (skill/config/industry_benchmarks.yaml).
6. Identify drivers: Volume / Price / Mix / Timing.
7. Assess profitability health.

## Output Structure
```
### 1. Data Overview
- Period, Currency, Basis (Accrual/Cash), Completeness

### 2. Profitability Dashboard
| Metric | Current | Prior/Budget | Var Abs | Var % | Benchmark | Status |
|--------|---------|--------------|---------|-------|-----------|--------|

### 3. Margin Analysis
- Gross Margin: X% (vs Y% prior) — interpretation
- EBITDA Margin, Net Margin likewise

### 4. Driver Analysis
- Revenue change driven by: ...
- Cost change driven by: ...

### 5. Health & Risks
- Rating: ...
- Risks: ...

### 6. Recommendations
1. ...
```

## Rules
- If revenue or cost missing, do NOT assume zero — flag as gap.
- Show formulas when first used.
- Distinguish recognized revenue vs contracted sales vs collected cash (IFRS 15 awareness).

## Language
Respond in user's language. Keep financial terms bilingual on first mention.
