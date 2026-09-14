# Example Analysis — Q2 2025 (Using Mock Data)

> This example demonstrates the full output of the Skill when analyzing `example_financials.csv` + `example_cashflow.csv` + `example_project.md`.

---

## EXECUTIVE SUMMARY — Demo Development Company — Q2 2025

**Overall Financial Health:** ⚠️ **Watchlist**

*Stable profitability (Gross Margin 32%) but liquidity pressure emerging: runway ~2.8 months, collection efficiency 86.1% (target 88%), and sales rate 27.7% vs 29.8% budget.*

**Confidence:** Medium — construction cost breakdown not yet reconciled; aging detail for >180d bucket missing.

### Key Findings

| # | Finding | Value | vs Budget / Benchmark | Driver |
|---|---------|-------|-----------------------|--------|
| 1 | Gross Margin below target | 32.0% vs 35.0% budget (−3pts) | vs benchmark avg 35% | Construction cost overrun (COR 43.5M vs 39M budget, +11.5% Unfavorable) — steel/cement inflation + quantity overrun |
| 2 | Net Margin compressed | 10.9% vs 13.3% budget | vs benchmark 18% avg | Similarly driven by cost + higher interest |
| 3 | Sales slightly behind | 65 units vs 70 budget (−7.1%) | Sales Rate 27.7% vs 29.8% | Velocity 5% below plan — market softness in 2BR segment |
| 4 | Collection efficiency below target | 86.1% vs 88.0% budget | Threshold 85% (still above warning) | Due EGP 67.4M, collected 58M — 9.4M overdue; 91-180d bucket EGP 22M |
| 5 | Cash approaching peak funding | Cumulative trough ~ -77.9M at Month 9 | vs plan -65M | Inflow delay (collections -4M vs plan) + outflow +4.5M |

### Financial Performance (Q2 2025)

| Metric | Actual | Budget | Var Abs | Var % | Class | Prior Q (Q1 25) | YoY (Q2 24) |
|--------|--------|--------|---------|-------|-------|-----------------|-------------|
| Revenue | 64.0M | 60.0M | +4.0M | +6.7% | Favorable | 58.0M | 52.0M |
| COR | 43.5M | 39.0M | +4.5M | +11.5% | Unfavorable | 40.0M | 35.8M |
| Gross Profit | 20.5M | 21.0M | -0.5M | -2.4% | Unfavorable | 18.0M | 16.2M |
| Gross Margin | 32.0% | 35.0% | -3.0pts | — | Unfavorable | 31.0% | 31.2% |
| S&M | 6.4M | 6.0M | +0.4M | +6.7% | Unfavorable | 5.8M | 5.2M |
| G&A | 3.5M | 3.2M | +0.3M | +9.4% | Unfavorable | 3.4M | 3.2M |
| EBITDA | 11.75M | 12.95M | -1.20M | -9.3% | Unfavorable | 9.95M | 8.8M |
| Net Profit | 6.98M | 7.98M | -1.01M | -12.6% | Unfavorable | 5.66M | 5.04M |
| Net Margin | 10.9% | 13.3% | -2.4pts | — | — | 9.8% | 9.7% |

**Margin Analysis:**
- Gross Margin 32% is 3pts below budget due to COR inflation. Construction cost per SQM estimated +8% vs budget. If trend continues, full-year gross margin may settle ~31-32% vs 35% target.
- EBITDA 11.75M (−9.3% vs budget) — operating leverage negative: revenue grew +6.7% but costs grew faster.
- Net Margin 10.9% vs benchmark avg 18% — below peer average; financing cost +0.1M above budget adds pressure.

### Project Performance (Green Valley Residence)

| Metric | Value | Target/Benchmark | Status |
|--------|-------|------------------|--------|
| GDV | 1,750.5M | — | — |
| GDC | 1,249.3M | — | — |
| Development Margin | 28.6% | 22% avg / 20% target | 🟢 Above target |
| Profit | 501.2M | — | — |
| Project IRR | 18.2% | 18% hurdle | 🟢 Meets hurdle (thin buffer) |
| NPV @15% | +58M | >0 | 🟢 Positive |
| Peak Funding | ~77.9M at M9 (financials) / 620M at M18 (full project) | — | Watch |
| Break-even | 71.4% sales (1,249M) | <70% healthy | 🟡 Slightly above healthy |
| Safety Margin | 28.6% | — | Adequate but not wide |

### Cash Flow & Liquidity

- **Peak Funding (15-month window):** EGP 77.9M negative at Month 9 (Aug-Sep 2025 trough)
- **Recovery:** Turns positive at Month 14 (Feb 2026)
- **Runway (if outflows continue):** ~2.8 months of cash burn (assuming EGP 35M avg monthly outflow vs closing -33.5M) — ⚠️ Critical: negative cumulative means reliance on facility.
- **Collection Efficiency:** 86.1% vs 88% budget — 9.4M overdue (13.9% of due)
- **DSCR (if debt service 2.2M/month):** Approx 0.9-1.1 in trough months — below 1.2 warning

### Risk Matrix (Top 3)

| # | Risk | Prob × Impact = Severity | Early Warning | Mitigation |
|---|------|--------------------------|---------------|------------|
| 1 | Liquidity / Peak Funding | High × High = Critical | Cumulative -77.9M vs -65M plan (+19.8% deeper) | Accelerate collections (target +8M in 60d), reschedule non-critical soft costs, confirm facility extension |
| 2 | Cost Overrun | Medium × High = High | COR +11.5% vs budget, 2 consecutive quarters over | Renegotiate bulk materials, review remaining BOQ, raise contingency 5%→7% |
| 3 | Sales Velocity | Medium × Medium = Medium | 65 vs 70 units (−7.1%) | Promote 2BR with flexible payment plan, no price discount >3% without IC approval |

### Recommendations (Prioritized)

| # | Action | Owner | Timeline | Impact |
|---|--------|-------|----------|--------|
| 1 | Weekly collection sprint on 91-180d overdue (EGP 22M) — daily follow-up, settlement incentives | Collection Manager | 60 days | +EGP 8-12M cash, efficiency → 90% |
| 2 | Review remaining construction BOQ for quantity overrun risk; value-engineer Phase 2 | PM + Cost Consultant | 14 days | Prevent +EGP 15M overrun |
| 3 | Renegotiate steel/cement bulk for next 6 months (lock price) | Procurement | 30 days | Save EGP 4-6M |
| 4 | Reforecast FY2025: Revenue 250M (vs 240M budget) but COR 172M (vs 156M) → Net ~22M (vs 28M) | Finance | 7 days | Accurate guidance for Board |
| 5 | Confirm financing facility headroom +20M to cover deeper peak | CFO | 14 days | Avoid liquidity gap |

### Assumptions & Limitations

- **Assumptions:** EGP currency, nominal values, discount rate 15% for NPV, construction S-curve per cash flow file, no FX adjustment beyond embedded inflation
- **Limitations:** Aging detail only summary, no IPC breakdown to separate quantity vs price, trial balance not provided — reliance on management accounts
- **Data Gaps:** Need BOQ detail, payment plan per unit type, facility agreement terms

---

## Sensitivity (Project-Level Illustration)

- **Price -10%:** IRR 18.2% → 11.5% (−6.7pts), Margin 28.6% → 20.7%
- **Cost +15%:** IRR 18.2% → 12.8% (−5.4pts), Margin → 18.2%
- **Delay +6 months:** IRR → 16.0% (−2.2pts)
- **Tornado #1:** Selling Price (spread 13.4pts), #2 Construction Cost (10.8pts)

## Scenario Table

| Metric | Best | Base | Worst |
|--------|-----:|-----:|------:|
| GDV | 1,890M | 1,750M | 1,575M |
| GDC | 1,162M | 1,249M | 1,436M |
| Profit | 728M | 501M | 139M |
| Margin | 38.5% | 28.6% | 8.8% |
| IRR | 28.4% | 18.2% | 6.5% |
| NPV | 182M | 58M | -85M |

---

*Generated by Real Estate Financial Analyst Skill v1.0 — for Board review.*
