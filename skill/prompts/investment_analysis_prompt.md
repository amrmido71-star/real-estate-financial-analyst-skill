# Prompt — Investment Analysis (IRR / NPV / Valuation)

You are performing **Investment & Valuation Analysis** for a real estate development project or portfolio.

## Inputs
- Cash flows (project-level and equity-level), Timeline, Initial investment/Equity
- Discount rate / WACC / Hurdle rate
- Comparable projects or market cap rates (if applicable)
- Financing structure (Debt %, rate, tenor)

## Metrics to Calculate
- **Project IRR & NPV** (unlevered)
- **Equity IRR & NPV** (levered, after debt service)
- **ROI, ROIC, Equity Multiple, Cash-on-Cash, Payback**
- **DSCR** if debt exists
- **Residual Land Value** (if land valuation needed)
- **GDV via Comparable** if comps provided

## Steps
1. Validate cash flow signs and timeline (initial outflow negative).
2. Calculate metrics with correct annualization.
3. Compare IRR to hurdle (from settings.yaml: default 18%). NPV >0 => value creating.
4. Scenario: Base / Best / Worst (define assumptions).
5. Sensitivity: Tornado of Price, Cost, Velocity, Rate, Delay.
6. Benchmark vs industry (industry_benchmarks.yaml).
7. Provide **Go / No-Go / Conditional** recommendation.

## Output Structure
```
### 1. Investment Overview
Structure, Equity, Debt, Timeline, Hurdle

### 2. Cash Flow Profile (Summary)
Timeline narrative + cumulative

### 3. Valuation Metrics
| Metric | Value | Hurdle/Benchmark | Verdict |
| IRR | 22% | 18% hurdle | ✅ Exceeds |
| NPV @15% | EGP 45M | >0 | ✅ Positive |
...

### 4. Scenario Analysis
| Metric | Best | Base | Worst |

### 5. Sensitivity (Tornado)
Rank drivers by impact on IRR/NPV

### 6. Risk-Adjusted View
Probability-weighted NPV, downside protection (break-even %)

### 7. Recommendation
Go / No-Go / Conditional — with price/cost/sales conditions
Key sensitivities to monitor
```

## Rules
- Show discount rate used and justify (WACC vs hurdle).
- If cash flows are monthly, annualize IRR correctly: (1+monthlyIRR)^12 −1.
- If equity cash flows missing, state: "Equity IRR cannot be computed — debt schedule required."
- Never present IRR without NPV (IRR can be misleading with non-conventional flows).

## Valuation Methods Reference
- DCF (primary for development)
- Residual Method (GDV − Costs − Profit = Land Value)
- Comparable (Price/SQM × Area)
See knowledge/valuation_methods.md
