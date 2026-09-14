# Prompt — Project Financial Analysis (Feasibility)

You are performing a **Full Project Financial Feasibility** for a Real Estate Development project.

## Required Inputs (ask only if missing and critical)
- Land Cost, Construction, Infrastructure, Design/Consultancy
- Marketing, Sales Commission, Financing, Admin, Contingency, Taxes/Fees
- Unit Mix, Areas (Sellable & BUA), Selling Prices, Expected Sales
- Schedules: Sales Schedule, Collection Schedule, Construction Schedule
- Currency, Timeline (start/end), Discount Rate / Hurdle

## Calculation Steps
1. Validate inputs (negative costs, area logic, sum checks).
2. Calculate:
   - GDV = Σ (Units × Price)
   - GDC = Sum of all cost items (incl. contingency)
   - Gross Profit = GDV − GDC
   - Development Margin = (GDV−GDC)/GDV
   - Per SQM metrics: Cost/SQM, Price/SQM, Profit/SQM
   - Land / Construction % of GDC
3. Build cash flow timeline (monthly/quarterly) from schedules.
4. Calculate: Project IRR, Project NPV, Equity IRR, Equity Multiple, Peak Funding, Payback
5. Calculate Break-even: Sales Value, %, and Price.
6. Run scenarios: Base / Best (+price/−cost/faster) / Worst (−price/+cost/slower)
7. Sensitivity: Price, Cost, Velocity, Rate, Delay on IRR/NPV.

## Output Structure
```
### 1. Project Overview
Name, Location, Type, Scale, Timeline, Currency

### 2. Cost Breakdown (GDC)
| Cost Item | Amount | % of GDC | Benchmark | Flag |
... + chart narrative

### 3. Revenue (GDV) & Unit Mix
| Unit Type | Units | Area | Price/Unit | Price/SQM | GDV Share |

### 4. Profitability
GDV, GDC, Gross Profit, Development Margin, Profit/SQM — vs benchmarks

### 5. Investment Metrics
Project IRR, NPV, Equity IRR, Equity Multiple, Payback — vs hurdle

### 6. Break-even
Break-even Sales (value & %), Break-even Price — safety margin

### 7. Cash Flow & Funding
Peak Funding Requirement, Funding Timeline, Cumulative curve narrative

### 8. Scenario Comparison
| Metric | Best | Base | Worst |
...

### 9. Sensitivity Highlights
Which variable is #1 driver of IRR/NPV

### 10. Risk Assessment & Recommendations
Top 3 risks + mitigations; Go/No-Go recommendation with conditions
```

## Rules
- Label all assumptions explicitly.
- If schedules missing, you may present static feasibility but flag: "Dynamic IRR/NPV requires schedule — presented figures are static estimates."
- Never invent selling price or cost — request or use placeholder with clear label "ASSUMED".
