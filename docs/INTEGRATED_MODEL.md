# Integrated Real Estate (V1.2.1 Hardening) Development Model V1.2

> Central Orchestrator — `ProjectAssumptions → … → Returns / Scenarios / Risk`  
> Monthly time engine, unit-level, auditable, bilingual (EN/AR)

## Architecture

```
assumptions.py (ProjectAssumptions: 7 groups, validate(), hash)
      ↓
integrated_model.py (IntegratedRealEstateModel)
      ├─ monthly engine: _months_between / _add_months / MonthlyRow(36 default)
      ├─ unit inventory: _build_units (equal or unit_mix premium)
      ├─ price escalation: if !price_lock_at_booking → (1+g)^years
      ├─ sales velocity: monthly_sales_schedule or velocity_units_per_month → monthly_units, contracted_sales, sale_dates
      ├─ collections: build_collection_schedule(schedule, handover_date) × collection_rate → monthly map YYYY-MM
      ├─ construction: generate_s_curve(budget, months, type) [+ escalation] → monthly curve
      ├─ costs: marketing/commission %GDV spread over sales months, soft/government/overheads spread monthly, contingency
      └─ financing: LTC draw (debt_pct × monthly cost capped by funding gap), interest accrued (capitalized vs cash), repayment from surplus, equity injection/distribution, net ≈0 when funded
      ↓
_calculate_returns → unlevered = collections - costs, levered = unlevered + draw - interest_cash - repay + draw, equity = -injection / +distribution (annualized (1+r)^12-1)
      ↓
_reconciliation → units_check, gdv_check, collections_check, cash_reconciliation (opening+net=closing), debt_reconciliation (opening+draw+interest_cap - repay=closing)
      ↓
health 0-100 (margin<20 -20, <15 -20, <10 Critical, peak>40%GDV -15, IRR<hurdle -20) → Healthy / Watch / Critical
      ↓
dashboard (sales/collections/construction/cashflow/returns) + ModelResult (gdv/gdc/profit/margin + IRR/NPV + peak_funding/debt/equity + reconciliation)
```

## Key Formulas

- **GDV** = Σ unit.price_per_unit (sold) — total sell-out value
- **GDC** = Σ total_development_cost (land+construction+soft+marketing+commission+gov+overhead+other+contingency+interest capitalized)
- **Profit** = GDV - GDC, **Margin** = Profit/GDV, **On Cost** = Profit/GDC
- **Peak Funding** = |min cumulative levered CF| (before equity), not net after equity (which is ~0)
- **IRR** = Newton-Raphson + bisection fallback on monthly CFs, annualized; hardened for billion-scale (overflow-safe `_npv_at`)
- **NPV** = Σ CF_t/(1+r_monthly)^t where r_monthly = (1+r_annual)^(1/12)-1; CF0 not discounted
- **MOIC** = total distributions / equity invested
- **MIRR / Multiple IRR** = `detect_multiple_irr` + `calculate_mirr`

## Assumptions Reference

| Group | Fields | Example Golden |
|-------|--------|----------------|
| Land | area_sqm, cost, transfer_fee | 80k sqm, 420M |
| Product | sellable, bua, unit_count, unit_mix, avg_price_per_sqm, growth, lock | 85k/110k, 300, 34k, 4%, lock=True |
| Sales | velocity, schedule, discount, cancellation | 9/mo, 2% |
| Collections | 5 buckets + during_build_months + post_handover_months + rate + lag | 10/10/35/25/20, 12/6, 90%, 0 |
| Construction | duration, budget, s_curve, escalation, contingency | 28mo, 1.05B, s_curve, 5% |
| Costs | design/consult/infra/gov/marketing%/commission%/overheads/other/contingency | 18M/22M/45M/12M/2.2%/2%/24M/10M/5% |
| Financing | debt_pct/equity_pct, interest, mode(capitalized/cash), LTC, tenor, bullet | 50/50, 13.5% cap, bullet |
| Project | start, end, currency, discount 14%, hurdle 18% | 2027-01-01→2029-12-31, EGP |

## Usage

```python
from skill.tools.models.assumptions import ProjectAssumptions, ProductAssumptions, LandAssumptions
from skill.tools.integrated_model import IntegratedRealEstateModel
from datetime import date

ass = ProjectAssumptions(
    project_name="My Compound",
    start_date=date(2027,1,1), end_date=date(2029,12,31),
    product=ProductAssumptions(sellable_area_sqm=50000, unit_count=150, avg_price_per_sqm=30000),
)
result = IntegratedRealEstateModel(ass).run()
print(result.gdv, result.profit, result.equity_irr, result.health_score)
print(result.dashboard)
```

Or golden:

```python
from examples.golden_project.assumptions import golden_assumptions
result = IntegratedRealEstateModel(golden_assumptions()).run()
assert result.reconciliation["cash_reconciliation"]
```

Runner for scenarios:

```python
from skill.tools.model_runner import ModelRunner
runner = ModelRunner(golden_assumptions())
scenarios = runner.run_scenarios({"selling_price_change_pct":10}, {"selling_price_change_pct":-10})
sens = runner.sensitivity("selling_price", [-20,-10,0,10,20])
tw = runner.two_way("selling_price", [-10,0,10], "construction_cost", [-10,0,10])
```

Validation & reporting:

```python
from skill.tools.model_validation import validate_reconciliation, audit_trail
from skill.tools.reporting import build_executive_summary

validate_reconciliation(result)  # {errors,warnings,info,is_valid}
audit_trail(result)  # run_id, hash, timestamp
build_executive_summary(result)  # markdown
```

## Engines

| Engine | Wraps | Key methods |
|--------|-------|-------------|
| RevenueEngine | project_metrics | gdv, net GDC, recognized |
| SalesEngine | sales_collection | velocity_schedule, inventory |
| CollectionEngine | sales_collection | build_schedule, aging |
| ConstructionEngine | construction_analysis | s_curve, EAC |
| FinancingEngine | financing | ltc, draw, DSCR |
| CashflowEngine | cashflow_analysis | build, waterfall |
| ReturnEngine | investment_metrics + valuation | irr, npv, mirr, wacc, break-even, dcf |
| ScenarioEngine | scenario_analysis | scenarios, sensitivity, tornado, Monte Carlo |

All engines are thin wrappers — no duplicated logic.

## Golden Case Audited Outputs

Run `python examples/golden_project/run.py`

- GDV 2.832B, GDC 1.846B, Profit 985M, 34.8% / 53.4% on cost
- Peak 305M, Debt 835M, Equity invested 305M, MOIC 1.97
- Equity IRR 30.4%, NPV 122M @14%, Healthy 100
- Scenarios rebuild end-to-end (not KPI scaling)
- Sensitivity monotonic; two-way matrix 3×3

## Reconciliation Checks

- Units: sold + available = total
- GDV: sum units == GDV
- Collections: sum collections ≈ GDV × collection_rate (within 1000 EGP, cutoff before post-handover may reduce)
- Cash: opening + net = closing per period
- Debt: opening + draw + interest_cap - repay = closing

All must be True for CI. See `tests/test_integrated_model.py`.

## Limitations & Roadmap

- Price escalation linear annual; FX not modeled
- Construction curve limited to 4 types + custom
- Debt repayment simplified (surplus → repay, else bullet); no amortizing schedule yet
- Tax on profit not yet in monthly CF (hurdle used)
- Monte Carlo optional in ScenarioEngine (sampling via normal/triangular/uniform, 1000 iter, P10/P50/P90)

## Version

- V1.2.1 — 2026-09-15 — Integrated model production, 166 tests, golden 300 units
- Backward compat: `from skill.tools.base_models import Unit` still works; `skill/tools/models.py` moved to `base_models.py`

