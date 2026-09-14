# Workflow — Budget vs Actual (Variance Analysis)

**Purpose:** Systematic variance analysis for management actions.
**Frequency:** Monthly / Quarterly
**Inputs:** Budget (original & revised if any), Actuals, Forecast

## Steps

### 1. Data Prep (10 min)
- Import Budget and Actual at same granularity (by account / project / month)
- Confirm budget version (original vs revised) — label clearly
- Check totals: sum(months) = annual budget?

### 2. Validation (5 min)
- Missing line items, sign errors (cost as negative?), date alignment
- Flag if Actual period ≠ Budget period

### 3. Calculate Variances (15 min)
For EACH line item:
```
Absolute Variance = Actual − Budget
% Variance = (Actual − Budget) / |Budget| × 100  (N/A if Budget=0)
Classification:
  Revenue/Collections: Actual > Budget → Favorable
  Cost/Outflows:       Actual > Budget → Unfavorable
  Neutral if |%| < 2%
Materiality: |%| ≥5% OR |Abs| ≥ threshold (e.g., EGP 500k) → Material
```
Use: `financial_calculations.calculate_variance` and `calculate_variance_pct`

### 4. Rank & Prioritize (10 min)
- Sort by |Absolute Variance| descending
- Top 5-10 material variances → deep dive
- Separate Favorable vs Unfavorable — do not net

### 5. Driver Analysis (20 min per material variance)
Decompose each:
- **Volume:** More/fewer units, more/fewer SQM built
- **Price:** Price per SQM, cost per SQM, unit price
- **Mix:** Shift to higher/lower margin units
- **Timing:** Recognized or paid earlier/later than budgeted (phasing)
- **Scope:** Added/removed scope (variation orders)
- **Inflation/FX:** Input price surge
- **One-off:** Non-recurring

Use prompt: `variance_analysis_prompt.md`

### 6. Cross-Check (10 min)
- Do variances reconcile to P&L total variance?
- Do cost variances explain margin change?
- Do collection variances explain cash variance?

### 7. Forecast Impact (10 min)
- Should full-year forecast be revised?
- Extrapolate: If trend continues, year-end variance = ?
- Recommend reforecast if material Unfavorable >5% for 2 consecutive months

### 8. Report (15 min)
- Use template: `templates/variance_report.md`
- Structure:
  1. Dashboard table (all lines, with Var & Class)
  2. Material Variances Deep Dive (driver + impact + recommendation per item)
  3. Overall Impact on Profit/Margin/Cash
  4. Forecast Revision proposal
  5. Action Items (Owner + Deadline)

## Example Commentary

> **Construction Cost: Budget 100M, Actual 112M, Var +12M (+12%) Unfavorable**
> - Drivers: BOQ quantity +6% (additional retaining walls, VO#3), Steel price +4% (EGP devaluation), Labour +2%
> - Impact: Gross Margin compressed from 35% to 31% (-4pts), Project IRR down ~1.8pts
> - Recommendation: Review remaining BOQ for similar overrun risk; renegotiate steel bulk for Phase 2; increase contingency from 5% to 7%; reforecast year-end construction to 135M

## Quality Checks
- [ ] Variances classified correctly (revenue vs cost opposite)
- [ ] No division by zero
- [ ] Commentary is driver-based, not generic
- [ ] Recommendations have owner & timeline
