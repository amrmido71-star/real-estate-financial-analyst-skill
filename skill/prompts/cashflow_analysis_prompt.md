# Prompt — Cash Flow Analysis & Forecast

You are performing **Cash Flow Analysis & Forecast** for a Real Estate Development entity/project.

## Inputs Expected
- Historical cash flows (Operating, Investing/Development, Financing) — or
- Forecast: Inflows (Collections, Sales Deposits, Financing Drawdowns) and Outflows (Land, Construction, Soft, S&M, Financing, Admin)
- Opening cash balance, Facility limits, Interest rate

## Steps
1. Validate: date sequence, cumulative logic, sign conventions, missing months.
2. Categorize:
   - Operating CF (Collections − Opex)
   - Development CF (Construction + Land + Soft outflows)
   - Financing CF (Loans drawn − repayments − interest)
   - Free CF = Operating + Development
   - Net CF = Free + Financing
   - Cumulative CF = Opening + Σ Net CF
3. Identify:
   - Peak Funding Requirement = minimum (most negative) Cumulative CF
   - Months of Runway = Cash / Avg Monthly Burn
   - Cash Conversion vs Profit (are profits turning into cash?)
4. Analyze Collections vs Revenue: Collection Efficiency, Aging.
5. Stress test: What if collections delay 2 months? Construction +15%? Sales −20%?

## Output Structure
```
### 1. Cash Flow Summary
| Period | Inflows | Outflows | Net CF | Cumulative | vs Budget |

### 2. Cash Flow Waterfall Narrative
How cash moved period-to-period

### 3. Peak Funding & Liquidity
Peak Requirement, Timing, Funding Gap, Runway

### 4. Collection vs Revenue
Contracted, Recognized, Collected — efficiency & aging

### 5. Risks
Liquidity, Collection, Financing — with Early Warning Indicators

### 6. Forecast Scenarios
Base / Stress — when does cash go negative?

### 7. Recommendations
Funding actions, collection acceleration, outflow rescheduling
```

## Rules
- Clearly separate Cash vs Accrual.
- Do not double-count financing inflows as revenue.
- Flag if forecast is overly optimistic vs historical collection rate.
