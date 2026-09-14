# Workflow — Management Reporting (Board / Executive Pack)

**Purpose:** Monthly/Quarterly board-ready reporting that drives decisions.
**Audience:** CEO, Board, Investment Committee
**Principle:** 1-page Executive Summary first, details after. Numbers → So What → Now What.

## Structure

### 1. Executive Summary (1 Page) — ALWAYS FIRST
Use template: `templates/executive_summary.md`

```
OVERALL HEALTH: Strong | Stable | Watchlist | Weak | Critical
(Justify in one sentence with KPIs)

KEY FINDINGS (3-5, prioritized):
1. [Metric] — [Value] — [vs Plan/Benchmark] — [Driver] — [Impact]

FINANCIAL PERFORMANCE (compact table):
Revenue | Gross Profit | Gross Margin | EBITDA | Net Profit | vs Budget

PROJECT PERFORMANCE (if applicable):
GDV | GDC | Development Margin | IRR | NPV | Peak Funding | Break-even

CASH FLOW:
Peak Funding Req., Runway, Collection Efficiency, DSCR

KEY RISKS (Top 3):
1. Risk — Probability×Impact=Severity — Early Indicator — Mitigation

RECOMMENDATIONS (3-5, actionable):
1. Action — Owner — Timeline — Expected Impact
  e.g., "Accelerate 91-180d collections (EGP 18M) — Collection Mgr — 60 days — +EGP 8M cash"

CONFIDENCE: High / Medium / Low (with gaps noted)
```

### 2. Detailed Financial Analysis (2-3 Pages)
- P&L waterfall: Revenue → Gross → EBITDA → Net with margins
- Vertical/Horizontal analysis
- Benchmark comparison
- Use template: `templates/financial_analysis_report.md`

### 3. Project Dashboard (1-2 Pages per project)
- Cost breakdown (GDC) with % and variance
- Revenue (GDV) by unit type
- Profitability: Margin, Profit/SQM
- Schedule status: Construction progress vs plan, Sales vs plan
- Use template: `templates/project_analysis_report.md`

### 4. Budget vs Actual (1 Page)
- Variance dashboard table
- Top 3 material variances deep dive (driver + impact + action)
- Use template: `templates/variance_report.md`

### 5. Cash Flow & Liquidity (1 Page)
- Forecast table + cumulative curve narrative
- Peak funding, runway, stress scenario
- Collection vs revenue bridge

### 6. Sales & Collections (1 Page)
- Sales funnel: Available → Reserved → Sold → Cancelled
- Collection: Contracted → Due → Collected → Overdue (aging)
- Inventory months, cancellation rate

### 7. Investment & Scenarios (if needed) (1-2 Pages)
- IRR/NPV vs hurdle, scenario table, sensitivity tornado
- Use template: `templates/investment_memo.md`

### 8. Risk Matrix (1 Page)
| Risk | Prob | Impact | Severity | Indicator | Action | Owner |

### 9. Appendix
- Assumptions, Data Sources, Limitations, Data Gaps, Formulas
- Glossary: Arabic (English) terms

## Writing Rules

### Do
- Start every section with insight, not number: "Gross Margin compressed 4pts to 31% driven by construction overrun — requires contingency review"
- Use active voice, short sentences
- Prioritize: Most important finding first
- Quantify: Always with value, %, and vs what
- Color coding narrative: 🟢 On track, 🟡 Watch, 🔴 Action needed

### Don't
- Don't dump tables without commentary
- Don't use generic recommendations ("improve sales")
- Don't hide bad news — flag early
- Don't mix cash and accrual without label

## Review Checklist Before Distribution
- [ ] Executive Summary fits 1 page (or 1 screen)
- [ ] Health Rating justified
- [ ] Every variance has driver and recommendation
- [ ] Numbers tie (P&L total = sum(lines), Cash cumulative logic)
- [ ] Assumptions & gaps stated
- [ ] Language matches audience (Arabic/English)
- [ ] No fabricated data — confidence stated
- [ ] CFO review completed

## Distribution
- Board Pack: PDF + Excel appendix
- Monthly Ops: Slide + Excel
- Archive: Versioned in /reports/YYYY-MM/
