# Workflow — Investment Analysis (IRR / NPV / Valuation)

**Purpose:** Investment decision for project, portfolio, or land acquisition.
**When:** Investment Committee, Land Bid, Project Prioritization
**Inputs:** Cash Flows (Project & Equity), Discount Rate, Financing Structure, Comps

## Steps

### 1. Define Scope (10 min)
- Project vs Equity view? (Unlevered vs Levered)
- Timeline, currency, inflation (nominal vs real)
- Hurdle rate source: WACC, target IRR, or cost of equity — document

### 2. Cash Flow Validation (10 min)
- Signs: Initial investment negative, inflows positive
- Period alignment: monthly vs yearly — annualize consistently
- No gaps, dates sequenced
- Check for non-conventional flows (multiple sign changes — IRR may be multiple)

### 3. Calculate Core Metrics (20 min)
| Metric | Function | Benchmark |
|--------|----------|-----------|
| Project IRR (unlevered) | `investment_metrics.calculate_irr` | > Hurdle (e.g., 18%) |
| Project NPV | `investment_metrics.calculate_npv` | >0 |
| Equity IRR | same on equity CFs | > Cost of Equity |
| Equity Multiple | `calculate_equity_multiple` | >1.8 good |
| ROI / ROIC | `calculate_roi` | vs target |
| Payback | `calculate_payback_period` | < threshold |
| DSCR (if debt) | `cashflow_analysis.calculate_dscr` | >1.2 |
| Cash-on-Cash | `calculate_cash_on_cash` | vs rental yield |

- Use prompt: `investment_analysis_prompt.md`

### 4. Compare to Hurdle & Benchmarks (10 min)
- IRR vs hurdle: exceed by how much? 
- NPV magnitude: value creation in currency
- Show both — IRR alone is insufficient

### 5. Scenario Analysis (15 min)
| Scenario | Price | Cost | Velocity | Collection | Rate |
|----------|-------|------|----------|------------|------|
| Best | +8% | −7% | ×0.8 time | +5% | −1% |
| Base | Plan | Plan | Plan | Plan | Plan |
| Worst | −10% | +15% | ×1.3 time | −10% delay | +2% |

- Use: `scenario_analysis.run_scenarios` → comparison table

### 6. Sensitivity (15 min)
- One-variable-at-a-time:
  - Price ±10% (5 steps: −10, −5, Base, +5, +10)
  - Cost ±15%
  - Delay ±6 months
  - Rate ±2%
- Output: Sensitivity matrix + Tornado ranking
- Use: `scenario_analysis.run_sensitivity_analysis`

### 7. Break-even & Downside (10 min)
- Break-even sales % and price (project_metrics)
- At what price drop does NPV hit zero?
- Safety margin commentary

### 8. Risk-Adjusted View (10 min)
- Probability-weighted NPV (if probabilities assigned)
- Downside protection assessment
- Concentration check

### 9. Valuation Cross-Check (10 min)
- Residual land value check (if land valuation)
- Comparable check for GDV reasonableness
- See: `knowledge/valuation_methods.md`

### 10. Recommendation (15 min)
- **Go / No-Go / Conditional** with conditions:
  - Go if: IRR 22% > hurdle, NPV positive across Worst, break-even 55% (safe)
  - Conditional: Go if price maintained > EGP 18k/SQM and cost cap enforced
  - No-Go: IRR < hurdle even in Best, or margin <10%
- Key sensitivities to monitor monthly
- Use template: `templates/investment_memo.md`

## Deliverables
- [ ] Investment Memo (2-3 pages) — board-ready
- [ ] Metrics table (IRR/NPV/Multiple/Payback vs hurdle)
- [ ] Scenario & Sensitivity tables + Tornado narrative
- [ ] Break-even analysis
- [ ] Assumptions & Limitations appendix

## Quality Gate
- [ ] Discount rate justified and labeled (nominal/real)
- [ ] Monthly vs annual IRR correctly annualized
- [ ] NPV and IRR presented together
- [ ] No fabricated cash flows
- [ ] Confidence level stated
