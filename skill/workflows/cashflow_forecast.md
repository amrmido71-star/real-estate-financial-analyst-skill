# Workflow — Cash Flow Forecast & Liquidity Analysis

**Purpose:** Forecast cash, identify peak funding, ensure liquidity.
**Frequency:** Monthly rolling (13-week + 12-month)
**Inputs:** Opening Cash, Sales Plan, Collection Plan, Construction Schedule, Cost Budgets, Financing Facilities

## Steps

### 1. Baseline Check (10 min)
- Opening cash balance confirmed (bank vs book)
- Facility limits, undrawn amounts, interest rates, repayment schedule
- Last actual cash flow — validate cumulative logic

### 2. Inflow Forecast (20 min)
| Inflow Type | Modeling |
|-------------|----------|
| Collections (installments) | Sales Velocity × Payment Plan × Collection Efficiency (e.g., 90%) |
| New Sales Deposits | Sales Plan × Down Payment % |
| Financing Drawdowns | Per facility agreement & construction milestones |
| Other | Rental, other income |

- Apply haircut: Not 100% collected on time — use historical efficiency
- Escrow adjustment if applicable (collections locked)

### 3. Outflow Forecast (20 min)
| Outflow Type | Modeling |
|--------------|----------|
| Land | Upfront or phased |
| Construction (IPC) | S-curve or BOQ monthly schedule |
| Infrastructure | Phased |
| Soft (Design/PM) | Front-loaded |
| S&M | Launch peaks, then ongoing |
| Financing | Interest + principal per schedule |
| Admin/G&A | Monthly run-rate |
| Taxes/Fees | Milestone-based |

- Construction S-curve example (36-month): 5%, 10%, 20%, 30%, 25%, 10% per 6-month block — calibrate to project

### 4. Net & Cumulative (10 min)
- Net CF per period = Inflows − Outflows + Financing Net
- Cumulative = Opening + Σ Net CF
- Use: `cashflow_analysis.analyze_cashflow`

### 5. Key Outputs (10 min)
- **Peak Funding Requirement** = |MIN(Cumulative)| — facility size needed
- **Peak Timing** = month of minimum
- **Runway** = Cash / Avg Burn (months)
- **DSCR** per period if debt exists
- **Variance vs Prior Forecast** — slippage commentary

### 6. Stress & Scenarios (15 min)
- **Stress Cases:**
  - Collections delayed 2 months
  - Construction cost +15%
  - Sales −30% for 6 months
  - Interest +2%
- Re-run cumulative — when does cash go negative? Need additional funding?

### 7. Risk Assessment (10 min)
- Liquidity Risk: Cumulative < 3 months burn? → Critical
- Collection Risk: Efficiency <85%? → Warning
- Financing Risk: DSCR <1.2? → Flag
- Concentration: Single inflow source >60%?

### 8. Report (15 min)
- Table: Month | Inflows | Outflows | Net | Cumulative | vs Budget
- Narrative: Waterfall commentary + Peak Funding story
- Chart description: Cumulative curve (down then up) — mark peak
- Recommendations: Accelerate collections, reschedule outflows, draw facility, equity injection
- Use template: `templates/financial_analysis_report.md` (Cash Flow section) or custom

## Validation
- Cumulative must tie: Opening + Σ Net = Closing
- Inflows not double-counted as revenue
- Financing inflows/outflows separated from operating
- Dates sequenced, no gaps

## Automation
```python
from skill.tools.cashflow_analysis import calculate_cumulative_cashflow, calculate_peak_funding, analyze_cashflow
forecast = analyze_cashflow(inflows, outflows, financing, opening_cash)
```

## Deliverables
- [ ] 12-24 month rolling forecast (monthly)
- [ ] Peak Funding memo
- [ ] Stress test summary
- [ ] Action plan (collection acceleration, cost rescheduling, facility management)
