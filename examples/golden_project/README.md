# Golden Project — Integrated Model V1.2

**Project:** East Cairo Compound, New Capital, Egypt  
**Scale:** 300 units (200 apartments 120sqm + 70 townhouses 220sqm + 30 villas 400sqm)  
**Timeline:** 2027-01-01 → 2029-12-31 (36 months, construction 28 months s-curve)  
**Currency:** EGP  
**Version:** 1.2.0 (audited)

This is the **canonical regression case**. Every release must reproduce these KPIs within 1% or justify variance.

## Assumptions Snapshot

| Category | Value |
|---|---|
| Land | 80,000 sqm — 420M EGP |
| Sellable | 85,000 sqm — avg 32,000 EGP/sqm |
| Unit mix | priced individually, avg blended GDV ~2.7-2.9B |
| Velocity | 9 units/month |
| Collections | 10% booking / 10% contract / 35% during-build (12mo) / 25% handover / 20% post (6mo), 90% collection rate |
| Construction | 1.45B budget, s-curve, 6% annual escalation |
| Costs | design 18M + consultants 22M + infra 45M + gov 12M + marketing 2.2% GDV + commission 2.0% + overheads 24M |
| Financing | 50% debt @13.5% capitalized, LTC 55% bullet, 50% equity |
| Discount/Hurdle | 14% / 18% |

## Expected Outputs (base case — for CI)

Run `python examples/golden_project/run.py` to regenerate.

Approximate audited band (Dec 2026):

- **GDV** 2.65–2.95B (depends on mix premium)
- **GDC** 2.05–2.25B
- **Profit** 500–700M
- **Margin** 18–26%
- **Peak Funding** 400–700M (levered cumulative minimum)
- **Equity IRR** 22–38% (monthly→annualized)
- **Equity NPV @14%** positive in base/best, negative in stress
- **Health** Healthy/Watch (score 75–100 base)
- **Reconciliation** cash ✓ debt ✓ gdv ✓

If your numbers drift outside, check: price escalation, s-curve vs custom, collection handover timing, interest capitalized vs cash.

## Files

- `assumptions.py` — `golden_assumptions()` factory + best/worst/stress deltas
- `run.py` — full pipeline: base → validation → scenarios (true cascade) → sensitivity → dashboard → executive summary
- `expected_metrics.json` — frozen metrics for automated diff

## Portfolio Extension (500+ units)

For portfolio 500+ units, combine this Golden Project with two sample projects in `examples/example_project.md` and `skill/tools/portfolio_analysis.py`:

- Project A — this Golden (300 units)
- Project B — West Cairo mid-income (180 units, GDV ~1.2B)
- Project C — North Coast chalets (80 units, GDV ~0.9B)

Run `portfolio_analysis` to see GDV/GDC/weighted margin/ranking.

## How to Use as Test

```python
from examples.golden_project.assumptions import golden_assumptions
from skill.tools.integrated_model import IntegratedRealEstateModel

result = IntegratedRealEstateModel(golden_assumptions()).run()
assert result.reconciliation["cash_reconciliation"]
assert result.reconciliation["debt_reconciliation"]
assert result.gdv > 2_500_000_000
assert result.margin_pct > 15
```

CI runs this in `tests/test_integrated_model.py::test_golden_project_reconciliation`.
