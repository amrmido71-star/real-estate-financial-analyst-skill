# Prompt — Budget vs Actual (Variance Analysis)

You are performing **Budget vs Actual Variance Analysis**.

## Inputs
- Budget (by line item, by month/project)
- Actual (same granularity)
- Optional: Prior period, Forecast

## Calculation per Line Item
```
Absolute Variance = Actual − Budget
% Variance = (Actual − Budget) / |Budget| × 100  (if Budget ≠ 0, else N/A)
Classification:
  Revenue/Collections: Actual > Budget → Favorable
  Cost/Outflows:       Actual > Budget → Unfavorable
  Neutral if |%| < threshold (default 2%)
```

## Steps
1. Validate budgets sum to totals, actuals complete.
2. Compute variances for: Revenue, COR, Gross Profit, Opex, EBITDA, Net Profit, Sales, Collections, Construction Costs, Land, S&M, Financing, etc.
3. Rank variances by materiality (|Var| and |%|).
4. For each material variance (>5% or > threshold), propose drivers:
   - Volume effect (more/fewer units)
   - Price effect (price per unit/SQM)
   - Mix effect (unit mix shift)
   - Timing effect (recognition or cash timing)
   - Scope change (added/removed works)
   - Inflation / FX
   - One-off
5. Provide management commentary — not just numbers.

## Output Structure
```
### 1. Variance Dashboard
| Line Item | Budget | Actual | Var Abs | Var % | Class | Material? |

### 2. Material Variances Deep Dive
For each top 5:
- Var: +12M (+12%) Unfavorable
- Drivers: Quantity +8% (BOQ overrun), Unit price +4% (steel inflation)
- Impact on Margin / IRR / Cash
- Recommendation: ...

### 3. Overall Impact
How variances affect full-year forecast

### 4. Forecast Revision Needed?
Should budget be reforecast? By how much?

### 5. Recommendations (Owner + Timeline)
```

## Example
Construction Budget 100M, Actual 112M →
- Var +12M (+12%) Unfavorable
- Possible Drivers: BOQ quantity overrun, steel/cement price inflation, scope change, delay penalties
- Recommendation: Review IPCs, renegotiate supplier, adjust contingency, reforecast year-end to 135M (+10%)

## Rules
- Ask for budget basis if unclear (original vs revised).
- Do not net favorable and unfavorable — show gross.
