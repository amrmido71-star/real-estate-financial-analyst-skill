# Financial Analysis Rules — Senior Analyst Standards

## Rule 1: Never Fabricate Data
- If data missing for a metric, output: `N/A — Data Gap: [required fields]`
- Do not assume price, cost, or sales. If you must illustrate, label as `ILLUSTRATIVE ASSUMPTION: EGP 15,000/SQM (source: comp X, to be confirmed)`.
- Confidence Level must drop to Medium/Low if gaps exist.

## Rule 2: Validate Before Calculate
Run checks:
- [ ] Missing values in critical columns
- [ ] Duplicates (unit codes, transaction IDs)
- [ ] Negative revenue / area / units
- [ ] Sold > Total
- [ ] Dates: sale > today, collection < sale
- [ ] Totals: sum(parts) = total
- [ ] Budget totals = sum(months)
- [ ] Cumulative CF logic
- [ ] Collection > Contracted
If any fail, report in `Data Quality Findings` before results.

## Rule 3: Guard Every Division
```
if denominator == 0 or denominator is None:
    return None with message "Cannot calculate [Metric] — denominator is zero/missing. Required: [X]"
```
Never return inf or crash.

## Rule 4: Classify Variances Correctly
- Revenue/Inflows: Actual > Budget = Favorable
- Costs/Outflows: Actual > Budget = Unfavorable
- Neutral if |%| < 2% (configurable)
- Show both Absolute and % — one without the other misleads.

## Rule 5: Driver Analysis > Numbers
For any material variance or margin change, decompose:
- **Volume** (units sold / built)
- **Price** (price per unit / per SQM / cost per unit)
- **Mix** (share of high vs low margin units)
- **Timing** (recognition or cash shifted between periods)
- **Scope** (added/removed works)
- **Inflation/FX**
- **One-off**

Example: Revenue ↑ 12% = Volume ↑ 8% + Price ↑ 5% + Mix −1% (more small units).

## Rule 6: Separate Cash vs Accrual
- Label every figure: `Revenue (POC, Accrual)` vs `Collections (Cash)` vs `Contracted Sales (Bookings)`
- Never sum them.

## Rule 7: Show Formulas Once, Then Apply
First time a metric appears, show formula in footnote or parenthesis.

## Rule 8: Benchmark Comparison
- Compare margin, IRR, sales rate, collection efficiency to industry_benchmarks.yaml
- State: "Gross Margin 28% vs benchmark avg 35% — below average, driver: land cost 32% vs typical 22%"

## Rule 9: Risk Scoring
For each risk: Probability (H/M/L) × Impact (H/M/L) = Severity (Critical/High/Medium/Low)
Provide Early Warning Indicator and Action.

## Rule 10: Scenario Discipline
- Base = most likely (management plan)
- Best = optimistic but plausible (not fantasy)
- Worst = plausible stress (not apocalypse) — should still be possible
- All three use **same model**, only assumptions change — show assumption table.

## Rule 11: Sensitivity Ranking
- Tornado: rank variables by impact on IRR/NPV.
- Must test at least: Price ±10%, Cost ±15%, Delay ±6 months, Rate ±2%.

## Rule 12: Management-Ready Output
- Executive Summary first (1 page): Health, Top Findings, Top Risks, Top Recommendations
- Details after.
- Recommendations: Specific, Actionable, Prioritized, with Owner & Timeline suggestion.
  - Bad: "Improve collections"
  - Good: "Assign dedicated collection officer to 91-180 day bucket (EGP 18M); weekly follow-up; target +EGP 8M in 60 days — Owner: Collection Manager"

## Rule 13: Label Assumptions & Limitations
- End every report with:
  - **Assumptions:** (discount rate 15%, EGP, no FX, etc.)
  - **Limitations:** (no aging detail, no BOQ, etc.)
  - **Data Gaps:** (need IPC breakdown, need payment plan)

## Rule 14: Language
- Respond in user's language.
- First mention: Arabic (English), e.g., هامش التطوير (Development Margin)
- Numbers: 1,234,567.89 — currency code before.

## Rule 15: Confidence
- **High:** Complete data, validated, benchmarked
- **Medium:** 1-2 gaps, assumptions on non-critical items
- **Low:** Material gaps, heavy assumptions — flag to user: "Recommend validating with actuals before decision"
