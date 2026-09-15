"""
integrated_model.py — Integrated Real Estate Development Financial Model V1.2
Central orchestrator: PROJECT ASSUMPTIONS → ... → RETURNS/SCENARIOS/RISK
Monthly time engine, unit-level, auditable.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any
from datetime import date, timedelta
import calendar
from collections import defaultdict

from .models.assumptions import ProjectAssumptions
from .models import Unit
from .investment_metrics import calculate_irr, calculate_npv, calculate_mirr
from .construction_analysis import generate_s_curve
from .sales_collection import build_collection_schedule
from .exceptions import InvalidAssumptionError
from .engines.financing_engine import FinancingEngine  # single source for financing


def _months_between(start: date, end: date) -> int:
    return (end.year - start.year) * 12 + (end.month - start.month) + 1

def _add_months(d: date, months: int) -> date:
    year = d.year + (d.month - 1 + months) // 12
    month = (d.month - 1 + months) % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

def _period_label(d: date) -> str:
    return d.strftime("%Y-%m")


@dataclass
class MonthlyRow:
    period: int
    label: str  # YYYY-MM
    date: date
    # Sales
    units_sold: int = 0
    contracted_sales: float = 0.0
    # Collections
    collections: float = 0.0
    # Costs
    land_cost: float = 0.0
    construction_cost: float = 0.0
    soft_cost: float = 0.0
    marketing_cost: float = 0.0
    commission_cost: float = 0.0
    government_fees: float = 0.0
    overheads: float = 0.0
    other_costs: float = 0.0
    contingency_cost: float = 0.0
    total_development_cost: float = 0.0
    # Financing
    debt_draw: float = 0.0
    debt_repayment: float = 0.0
    interest_accrued: float = 0.0
    interest_cash: float = 0.0
    opening_debt: float = 0.0
    closing_debt: float = 0.0
    equity_injection: float = 0.0
    equity_distribution: float = 0.0
    opening_equity: float = 0.0
    closing_equity: float = 0.0
    # Cash
    net_cash_flow: float = 0.0
    opening_cash: float = 0.0
    closing_cash: float = 0.0
    cumulative_cash_flow: float = 0.0
    # Progress
    construction_progress_pct: float = 0.0
    cumulative_construction_pct: float = 0.0


@dataclass
class ModelResult:
    assumptions: ProjectAssumptions
    run_id: str
    timestamp: str
    periods: List[MonthlyRow]
    # Aggregates
    gdv: float
    gdc: float
    profit: float
    margin_pct: float
    profit_on_cost_pct: float
    total_units: int
    sold_units: int
    remaining_units: int
    # Cash flow series
    unlevered_cash_flows: List[float]
    levered_cash_flows: List[float]
    equity_cash_flows: List[float]
    # Returns
    unlevered_irr: Optional[float]
    levered_irr: Optional[float]
    equity_irr: Optional[float]
    unlevered_npv: Optional[float]
    levered_npv: Optional[float]
    equity_npv: Optional[float]
    mirr: Optional[float]
    moic: Optional[float]
    equity_multiple: Optional[float]
    payback_period: Optional[float]
    # Funding
    peak_funding: float
    peak_equity: float
    peak_debt: float
    minimum_cash: float
    funding_gap: float
    # Reconciliation
    reconciliation: Dict[str, Any]
    # Health
    financial_health: str
    health_score: int
    # Dashboard (for reporting)
    dashboard: Dict[str, Any]


class IntegratedRealEstateModel:
    """
    Central Integrated Model. Usage:
        assumptions = ProjectAssumptions(...)
        model = IntegratedRealEstateModel(assumptions)
        result = model.run()
        result.gdv, result.irr, result.cashflow, etc.
    """

    def __init__(self, assumptions: ProjectAssumptions):
        self.assumptions = assumptions
        self.errors = assumptions.validate()
        if self.errors:
            raise InvalidAssumptionError("; ".join(self.errors))
        self._periods: List[MonthlyRow] = []
        self._units: List[Unit] = []

    def _build_units(self) -> List[Unit]:
        a = self.assumptions
        units = []
        # If product.unit_mix provided, use it
        if a.product.unit_mix:
            idx = 0
            for mix in a.product.unit_mix:
                count = mix.get("count", mix.get("units", 0))
                for i in range(count):
                    area = mix.get("area_sqm", 100)
                    pps = mix.get("price_per_sqm", a.product.avg_price_per_sqm)
                    # Apply discount
                    list_price = area * pps
                    net_price = list_price * (1 - a.sales.discount_pct/100)
                    units.append(Unit(
                        unit_code=f"U{idx+1:04d}",
                        unit_type=mix.get("type", "unit"),
                        area_sqm=area,
                        price_per_unit=net_price,
                        status="available"
                    ))
                    idx += 1
        else:
            # Generic: equal units
            n = a.product.unit_count
            area = a.product.sellable_area_sqm / n if n else 0
            pps = a.product.avg_price_per_sqm
            for i in range(n):
                # Price escalation per year if lock is False? For now, base price
                list_price = area * pps
                net_price = list_price * (1 - a.sales.discount_pct/100)
                units.append(Unit(
                    unit_code=f"U{i+1:04d}",
                    unit_type="standard",
                    area_sqm=area,
                    price_per_unit=net_price,
                    status="available"
                ))
        self._units = units
        return units

    def _apply_price_escalation(self, units: List[Unit], sales_dates: List[date]) -> List[Unit]:
        """If price_lock_at_booking is False, escalate price for later sales"""
        a = self.assumptions
        if a.product.price_lock_at_booking or a.product.price_growth_annual_pct == 0:
            return units
        # Escalate: price * (1+g)^years_since_start
        start = a.start_date
        for unit, sdate in zip(units, sales_dates):
            years = (sdate - start).days / 365.25
            factor = (1 + a.product.price_growth_annual_pct/100) ** years
            # Recompute price (keep area same)
            base_pps = a.product.avg_price_per_sqm
            new_pps = base_pps * factor
            unit.price_per_unit = unit.area_sqm * new_pps * (1 - a.sales.discount_pct/100)
            unit.price_per_sqm = new_pps
        return units

    def _build_sales_plan(self, units: List[Unit]) -> Tuple[List[int], List[float], List[date]]:  # noqa: C901
        """Returns monthly_sales_units, contracted_sales, sale_dates_per_unit"""
        a = self.assumptions
        total_units = len(units)
        months = _months_between(a.start_date, a.end_date)
        # Determine monthly sales schedule
        if a.sales.monthly_sales_schedule:
            monthly_units = list(a.sales.monthly_sales_schedule)
            # Pad/truncate to months
            if len(monthly_units) < months:
                monthly_units += [0] * (months - len(monthly_units))
            else:
                monthly_units = monthly_units[:months]
        else:
            # Velocity-based: distribute evenly, but front-loaded a bit
            vel = a.sales.velocity_units_per_month
            # Cap by remaining
            monthly_units = []
            remaining = total_units
            for m in range(months):
                if remaining <= 0:
                    monthly_units.append(0)
                else:
                    sell = min(int(round(vel)), remaining)
                    # Add variability: sales faster early, slower late (simple)
                    # For now constant
                    monthly_units.append(sell)
                    remaining -= sell
            # If still remaining due to rounding, distribute
            # Adjust to exactly match total_units
            total_sold = sum(monthly_units)
            if total_sold < total_units:
                # Add remainder to early months
                for i in range(total_units - total_sold):
                    monthly_units[i % months] += 1
            elif total_sold > total_units:
                # Remove excess from end
                excess = total_sold - total_units
                for i in range(len(monthly_units)-1, -1, -1):
                    if excess <=0:
                        break
                    take = min(monthly_units[i], excess)
                    monthly_units[i] -= take
                    excess -= take

        # Apply cancellation: reduce effective sales
        # For now, just track but don't reduce contracted immediately; will handle in collections
        # Build sale dates per unit
        sale_dates = []
        unit_idx = 0
        contracted_sales = []
        for m, count in enumerate(monthly_units):
            sale_date = _add_months(a.start_date, m)
            for _ in range(count):
                if unit_idx < len(units):
                    sale_dates.append(sale_date)
                    # Contracted value for this unit
                    # If escalation, need to compute per sale date (done separately)
                    contracted_sales.append(units[unit_idx].price_per_unit)
                    # Mark sold
                    units[unit_idx].status = "sold"
                    unit_idx += 1
        # If escalation, re-apply
        if not a.product.price_lock_at_booking and a.product.price_growth_annual_pct != 0:
            self._apply_price_escalation(units, sale_dates)
            # Recompute contracted_sales
            contracted_sales = [u.price_per_unit for u in units if u.status=="sold"]

        return monthly_units, contracted_sales, sale_dates

    def _build_collections(self, contracted_sales: List[float], sale_dates: List[date]) -> Dict[str, float]:
        """Build monthly collection map YYYY-MM -> amount"""
        a = self.assumptions
        schedule = a.collections.schedule()
        handover_date = _add_months(a.construction.start_date or a.start_date, a.construction.duration_months)
        monthly: Dict[str, float] = defaultdict(float)
        for value, sdate in zip(contracted_sales, sale_dates):
            events = build_collection_schedule(value, sdate, schedule, handover_date)
            for ev in events:
                # Apply collection rate and lag
                due = ev["due_amount"] * a.collections.collection_rate_pct/100
                # Apply lag
                due_date = ev["due_date"] + timedelta(days=30*a.collections.collection_lag_months)
                key = due_date.strftime("%Y-%m")
                monthly[key] += due
                # The uncollected portion (default) is lost (not collected)
                # For default rate, we could model write-off, but we already applied collection_rate
        return dict(monthly)

    def _build_construction_curve(self) -> List[float]:
        a = self.assumptions
        budget = a.construction.budget
        months = a.construction.duration_months
        # Apply escalation: compound annual
        # For simplicity, increase budget by escalation
        if a.construction.escalation_annual_pct != 0:
            years = months/12
            budget = budget * (1 + a.construction.escalation_annual_pct/100) ** years
        # Generate S-curve
        if a.construction.s_curve_type == "custom" and a.construction.custom_curve:
            weights = a.construction.custom_curve
            total_w = sum(weights)
            monthly = [budget * w/total_w for w in weights]
        else:
            type_map = {"linear":"linear","s_curve":"standard","front_loaded":"front_loaded","back_loaded":"back_loaded"}
            curve = type_map.get(a.construction.s_curve_type, "standard")
            monthly = generate_s_curve(budget, months, curve)
        return monthly

    def _build_monthly_cashflow(self) -> List[MonthlyRow]:  # noqa: C901
        a = self.assumptions
        months = _months_between(a.start_date, a.end_date)
        # Build units and sales
        units = self._build_units()
        monthly_units, contracted_sales, sale_dates = self._build_sales_plan(units)

        # Collections map
        collections_map = self._build_collections(contracted_sales, sale_dates)

        # Construction curve
        construction_monthly = self._build_construction_curve()
        # Align construction to start date
        construction_start_idx = 0
        if a.construction.start_date:
            construction_start_idx = _months_between(a.start_date, a.construction.start_date)
            construction_start_idx = max(0, construction_start_idx)
        # Other costs: distribute
        # Marketing: % of GDV, spread over sales period
        gdv = sum(contracted_sales) if contracted_sales else sum(u.price_per_unit for u in units)
        marketing_total = gdv * a.costs.marketing_pct_gdv/100
        commission_total = gdv * a.costs.commission_pct_gdv/100
        # Soft costs: distribute over construction duration
        soft_total = a.costs.design + a.costs.consultants + a.costs.infrastructure
        # Government, overheads, other: spread monthly
        gov_total = a.costs.government_fees
        overhead_total = a.costs.overheads
        other_total = a.costs.other

        # Contingency
        base_cost = a.construction.budget + soft_total
        contingency_total = base_cost * a.costs.contingency_pct/100 if not a.construction.contingency_included_in_gdc else 0
        # If contingency included, it's part of GDC but not separate cash flow? We'll still show as cost

        # Build periods — P0: build actual sales map for accurate monthly aggregation
        # sales_by_label: YYYY-MM -> sum of contracted values for that month (unit-level truth)
        sales_by_label: Dict[str, float] = defaultdict(float)
        # Also need contracted_sales and sale_dates from _build_sales_plan; gdv already sum
        for sdate, cval in zip(sale_dates, contracted_sales):
            sales_by_label[_period_label(sdate)] += cval

        periods: List[MonthlyRow] = []
        # For financing: track debt — single source of truth is this model (FinancingEngine wraps this logic)
        opening_debt = 0.0
        opening_cash = 0.0
        opening_equity = 0.0
        cumulative = 0.0

        # Precompute total GDC for break-even etc. (but done after)
        for m in range(months):
            pdate = _add_months(a.start_date, m)
            label = _period_label(pdate)
            row = MonthlyRow(period=m, label=label, date=pdate)
            # Sales — actual unit-level aggregation (P0 fix: no avg approximation)
            row.units_sold = monthly_units[m] if m < len(monthly_units) else 0
            # Contracted sales: sum of actual unit prices for units sold in this month label
            # Built from sale_dates/contracted_sales mapping to avoid avgPrice distortion
            # sales_by_label is computed before loop (see below)
            row.contracted_sales = sales_by_label.get(label, 0.0)

            # Collections
            row.collections = collections_map.get(label, 0.0)

            # Costs timing
            # Land: at acquisition date or month 0
            if m == 0:
                # Land cost at start (or acquisition date month)
                land_cost = a.land.cost if a.costs.land == 0 else a.costs.land
                row.land_cost = land_cost
            # Construction
            # construction_monthly index relative to construction start
            cons_idx = m - construction_start_idx
            if 0 <= cons_idx < len(construction_monthly):
                row.construction_cost = construction_monthly[cons_idx]
            # Soft: spread over construction
            if 0 <= cons_idx < len(construction_monthly) and soft_total >0:
                # Distribute soft proportionally to construction duration
                row.soft_cost = soft_total / len(construction_monthly) if len(construction_monthly) else 0
            # Marketing: spread over sales months (or first 12 months)
            sales_months = sum(1 for u in monthly_units if u>0)
            if sales_months and m < sales_months:
                row.marketing_cost = marketing_total / sales_months if sales_months else 0
                row.commission_cost = commission_total / sales_months if sales_months else 0
            # Gov/overheads/other spread over all months
            row.government_fees = gov_total / months if months else 0
            row.overheads = overhead_total / months if months else 0
            row.other_costs = other_total / months if months else 0
            row.contingency_cost = contingency_total / months if months else 0

            row.total_development_cost = (row.land_cost + row.construction_cost + row.soft_cost +
                                         row.marketing_cost + row.commission_cost + row.government_fees +
                                         row.overheads + row.other_costs + row.contingency_cost)

            # Financing: LTC-based draw + interest — Single Source via FinancingEngine
            total_month_need = row.total_development_cost - row.collections
            row.debt_draw = FinancingEngine.debt_draw_for_gap(
                total_cost=row.total_development_cost,
                debt_pct=a.financing.debt_pct,
                collections=row.collections,
                total_need=total_month_need,
            )
            row.opening_debt = opening_debt
            row.interest_accrued = FinancingEngine.monthly_interest(opening_debt, a.financing.interest_rate_annual_pct)
            # Debt repayment: use surplus collections after costs+interest to repay
            surplus_after_costs = row.collections - row.total_development_cost - (0 if a.financing.interest_payment_mode=="capitalized" else row.interest_accrued)
            # Actually repayment comes from surplus after covering costs
            # Simpler: if collections > costs + interest, use excess to repay debt
            if surplus_after_costs > 0 and opening_debt + row.debt_draw > 0:
                # Repay up to outstanding
                row.debt_repayment = min(opening_debt + row.debt_draw + (row.interest_accrued if a.financing.interest_payment_mode=="capitalized" else 0), surplus_after_costs)
            else:
                row.debt_repayment = 0

            # Capitalized vs Cash — P0: never double-count
            # capitalized: interest → debt (cash 0), closing = opening + draw + accrued - repay
            # cash: interest → cash outflow, closing = opening + draw - repay
            if a.financing.interest_payment_mode == "capitalized":
                row.interest_cash = 0
                row.closing_debt = opening_debt + row.debt_draw + row.interest_accrued - row.debt_repayment
            else:
                row.interest_cash = row.interest_accrued
                row.closing_debt = opening_debt + row.debt_draw - row.debt_repayment

            # Equity: covers remaining need after debt
            remaining_need = row.total_development_cost + row.interest_cash + row.debt_repayment - row.collections - row.debt_draw
            if remaining_need > 0:
                row.equity_injection = remaining_need
            else:
                row.equity_injection = 0
                # Surplus after debt repayment is distribution
                surplus_for_equity = row.collections + row.debt_draw - row.total_development_cost - row.interest_cash - row.debt_repayment
                row.equity_distribution = max(0, surplus_for_equity)

            row.opening_equity = opening_equity
            row.closing_equity = opening_equity + row.equity_injection - row.equity_distribution

            # Cash flows
            row.net_cash_flow = (row.collections + row.debt_draw + row.equity_injection
                                 - row.total_development_cost - row.interest_cash - row.debt_repayment - row.equity_distribution)
            # net should be ~0 (funded), distributions handle surplus

            row.opening_cash = opening_cash
            row.closing_cash = opening_cash + row.net_cash_flow
            cumulative += row.net_cash_flow
            row.cumulative_cash_flow = cumulative
            row.cumulative_construction_pct = row.cumulative_construction_pct if hasattr(row,'cumulative_construction_pct') else 0

            # Progress
            if construction_monthly:
                total_cons = sum(construction_monthly)
                row.construction_progress_pct = (row.construction_cost / total_cons * 100) if total_cons else 0
                row.cumulative_construction_pct = sum(r.construction_cost for r in periods + [row]) / total_cons * 100 if total_cons else 0

            # Update for next
            opening_debt = row.closing_debt
            opening_cash = row.closing_cash
            opening_equity = row.closing_equity

            periods.append(row)

        self._periods = periods
        return periods

    def _calculate_returns(self, periods: List[MonthlyRow]) -> Dict:
        # Unlevered: collections - total_development_cost (before financing)
        unlevered = [p.collections - p.total_development_cost for p in periods]
        # Levered: collections - total_development_cost - interest_cash - debt_repayment + debt_draw
        # But our net already includes equity, so levered = net - equity_injection + equity_distribution? For now:
        # Levered = unlevered - interest_cash - debt_repayment + debt_draw
        levered = []
        for p in periods:
            cf = p.collections - p.total_development_cost - p.interest_cash - p.debt_repayment + p.debt_draw
            levered.append(cf)
        # Equity: collections - total_development_cost - interest_cash - debt_repayment + debt_draw - equity? Simplified: net cash flow to equity
        # For investor, equity injection is outflow (negative), distribution is inflow (positive)
        # Our net = collections + debt + equity_in - costs - interest...
        # To get equity investor cash flow: -equity_injection + (if distribution) - but we have no distribution, so equity CF = -equity_injection + (if surplus after debt, it would be distribution)
        # Simplify: equity CF = -equity_injection + max(0, collections - costs - debt_service) ??? Let's approximate: equity CF = levered CF + (if positive, it's distribution)
        # For now, equity_cfs = [-equity_injection if injection>0 else levered if levered>0 else 0] — complex
        # Simplified: equity cash flows = levered cash flows but with initial equity outflows
        # We'll define equity_cfs as: at each period, -equity_injection + (if net positive and debt repaid, remainder is distribution)
        # For our simple model where equity_injection covers gap, net is 0 by construction (since equity fills gap), so equity_cfs would be -injection...
        # To avoid 0 net, we need to model properly: net should be collections - costs + debt - repayment, equity is separate.
        # Let's recalc: unlevered and levered are as above, equity = levered - equity_injection? Wait levered already includes debt, so equity investor sees: -equity injection at start, + distributions later (when collections > costs + debt service)
        # In our construction, equity_injection = max(0, need), and net = collections + debt + equity_in - costs - interest = 0 if need>0, or positive if collections > costs
        # So equity cash flow = -equity_injection + (if net positive after covering, it's distribution)
        # But net already includes equity_in, so to get equity investor view: equity_cf = -equity_injection + (net if net>0 else 0) ??? Let's do: equity_cf = -equity_injection + max(0, net) ??? But net includes equity_in, so double counts.
        # Simpler: define equity_cf = levered_cf : but levered_cf already is after debt, before equity. Then equity investor invests -equity needed and gets levered_cf positive later.
        # So we can set: equity_cfs = [-p.equity_injection if p.equity_injection>0 else p.collections - p.total_development_cost - p.interest_cash - p.debt_repayment + p.debt_draw for p]
        # Actually for periods where equity_injection>0, equity_cf = -equity_injection; for periods where no injection and levered>0, equity_cf = levered
        equity_cfs_simple = []
        for p in periods:
            if p.equity_distribution > 0:
                equity_cfs_simple.append(p.equity_distribution)
            elif p.equity_injection > 0:
                equity_cfs_simple.append(-p.equity_injection)
            else:
                # no injection/distribution: use levered (could be zero)
                equity_cfs_simple.append(levered[periods.index(p)])

        # Calculate IRRs: need to convert monthly to annual? For now monthly IRR then annualized
        # For yearly IRR, aggregate to annual
        # Simple: treat periods as months, but IRR on monthly series then annualize
        unlevered_irr_m = calculate_irr(unlevered) if any(unlevered) else None
        levered_irr_m = calculate_irr(levered) if any(levered) else None
        equity_irr_m = calculate_irr(equity_cfs_simple) if any(equity_cfs_simple) else None

        def annualize(mirr):
            return (1+mirr)**12 -1 if mirr is not None else None

        unlevered_irr = annualize(unlevered_irr_m)
        levered_irr = annualize(levered_irr_m)
        equity_irr = annualize(equity_irr_m)

        # NPV: use discount_rate annual, but need monthly rate
        dr_annual = self.assumptions.discount_rate_annual_pct/100
        dr_monthly = (1+dr_annual)**(1/12) -1
        unlevered_npv = calculate_npv(unlevered, dr_monthly)
        levered_npv = calculate_npv(levered, dr_monthly)
        equity_npv = calculate_npv(equity_cfs_simple, dr_monthly)

        # Also annual NPV for reporting (aggregate to annual)
        # Simplify: use monthly NPV as proxy

        # MIRR, MOIC
        # MOIC = total distributions / total equity invested
        total_equity_invested = sum(p.equity_injection for p in periods)
        total_distributions = sum(max(0, cf) for cf in equity_cfs_simple)
        moic = total_distributions / total_equity_invested if total_equity_invested else None
        # For MIRR, use finance 10%, reinvest 12% as default
        mirr = calculate_mirr(equity_cfs_simple, 0.10, 0.12) if equity_cfs_simple and any(equity_cfs_simple) else None
        mirr_annual = annualize(mirr) if mirr and abs(mirr)<1 else mirr  # mirr already monthly? Actually calculate_mirr on monthly gives monthly, so annualize

        # Payback: on equity
        from .investment_metrics import calculate_payback_period
        payback = calculate_payback_period(equity_cfs_simple)

        return {
            "unlevered_cash_flows": unlevered,
            "levered_cash_flows": levered,
            "equity_cash_flows": equity_cfs_simple,
            "unlevered_irr": unlevered_irr,
            "levered_irr": levered_irr,
            "equity_irr": equity_irr,
            "unlevered_irr_monthly": unlevered_irr_m,
            "levered_irr_monthly": levered_irr_m,
            "equity_irr_monthly": equity_irr_m,
            "unlevered_npv": unlevered_npv,
            "levered_npv": levered_npv,
            "equity_npv": equity_npv,
            "mirr": mirr_annual,
            "moic": moic,
            "equity_multiple": moic,
            "payback_period": payback,
            "total_equity_invested": total_equity_invested,
            "total_distributions": total_distributions,
        }

    def _reconciliation(self, periods: List[MonthlyRow], gdv: float, gdc: float) -> Dict:
        # Units
        total_units = len(self._units)
        sold = sum(1 for u in self._units if u.status=="sold")
        available = sum(1 for u in self._units if u.status=="available")
        # GDV check
        sum_unit_sales = sum(u.price_per_unit for u in self._units if u.status=="sold")
        gdv_check = abs(sum_unit_sales - gdv) < 1.0
        # Collections check: sum collections vs sum installments? Total collections should <= gdv * collection_rate
        total_collections = sum(p.collections for p in periods)
        expected_collections = gdv * self.assumptions.collections.collection_rate_pct/100
        collections_check = abs(total_collections - expected_collections) < 1000  # allow small diff due to timing cut off? Actually if end_date cuts off post-handover, collections may be less
        # Cash: opening + net = closing
        cash_ok = True
        for p in periods:
            if abs(p.opening_cash + p.net_cash_flow - p.closing_cash) > 0.01:
                cash_ok = False
                break
        # Debt: opening + draw + interest_cap - repayment = closing — via FinancingEngine single source
        debt_ok = True
        for p in periods:
            capitalized = self.assumptions.financing.interest_payment_mode == "capitalized"
            # Use engine's reconciliation check for consistency
            if not FinancingEngine.debt_reconciliation_check(
                opening=p.opening_debt,
                draw=p.debt_draw,
                interest_accrued=p.interest_accrued,
                repayment=p.debt_repayment,
                closing=p.closing_debt,
                capitalized=capitalized,
                tol=0.01,
            ):
                debt_ok = False
                break
        # Construction reconciliation — P0 harden (no bypass)
        total_cons = sum(p.construction_cost for p in periods)
        budget = self.assumptions.construction.budget
        # Expected with escalation (compound annual on budget)
        months_escal = self.assumptions.construction.duration_months
        esc = self.assumptions.construction.escalation_annual_pct
        if esc:
            expected_cons = budget * (1 + esc/100) ** (months_escal/12)
        else:
            expected_cons = float(budget)
        variance = total_cons - expected_cons
        variance_pct = (variance / expected_cons * 100) if expected_cons else 0
        # Tolerance: 0.5% or 1000 EGP absolute (to handle rounding)
        tolerance = max(expected_cons * 0.005, 1000.0)
        cons_ok = abs(variance) <= tolerance

        return {
            "units_total": total_units,
            "units_sold": sold,
            "units_available": available,
            "units_check": sold + available <= total_units,
            "gdv_check": gdv_check,
            "gdv_vs_sum_units": {"gdv": gdv, "sum_units": sum_unit_sales, "match": gdv_check},
            "collections_check": collections_check,
            "total_collections": total_collections,
            "expected_collections": expected_collections,
            "cash_reconciliation": cash_ok,
            "debt_reconciliation": debt_ok,
            "construction_check": cons_ok,
            "total_construction": total_cons,
            "budget": budget,
            "expected_construction": expected_cons,
            "construction_variance": variance,
            "construction_variance_pct": variance_pct,
            "construction_tolerance": tolerance,
            "construction_status": "PASS" if cons_ok else "FAIL",
        }

    def _financial_health(self, returns: Dict, periods: List[MonthlyRow], reconciliation: Dict) -> Tuple[str, int, Dict]:
        """Determine health: Critical/Watch/Healthy with score 0-100"""
        score = 100  # noqa: F841
        issues: List[str] = []  # noqa: F841
        # Profitability
        profit = returns.get("gdv", 0) - returns.get("gdc", 0) if "gdv" in returns else 0  # noqa: F841
        # Use actual gdv/gdc from result
        # We'll compute outside

        # For now, use returns dict passed from run (contains gdv/gdc)
        # This is placeholder; actual health computed in run() after gdv/gdc known
        return "Healthy", 100, {}

    def run(self) -> ModelResult:  # noqa: C901
        import datetime
        a = self.assumptions
        # Build cashflow
        periods = self._build_monthly_cashflow()
        # Aggregates
        gdv = sum(u.price_per_unit for u in self._units if u.status=="sold")  # noqa: F841
        # If not all sold, gdv is sold only; but for feasibility, GDV should be total potential (all units). Use total units price
        gdv_total = sum(u.price_per_unit for u in self._units)
        # For reporting, use gdv_total as GDV (sell-out value)
        gdv_report = gdv_total
        gdc = sum(p.total_development_cost for p in periods)
        profit = gdv_report - gdc
        margin = (profit / gdv_report * 100) if gdv_report else 0
        profit_on_cost = (profit / gdc * 100) if gdc else 0

        total_units = len(self._units)
        sold_units = sum(1 for u in self._units if u.status=="sold")

        returns = self._calculate_returns(periods)
        # Add gdv/gdc to returns for health
        returns["gdv"] = gdv_report
        returns["gdc"] = gdc

        # Reconciliation
        recon = self._reconciliation(periods, gdv_report, gdc)

        # Peak funding: based on cumulative LEVERED cash flow (before equity injections) to show true funding need
        # net after equity is ~0, so use levered cumulative
        levered_cum = []
        cum = 0
        for cf in returns["levered_cash_flows"]:
            cum += cf
            levered_cum.append(cum)
        min_levered = min(levered_cum) if levered_cum else 0
        peak_funding = abs(min_levered) if min_levered < 0 else 0
        # For dashboard minimum_cash, show levered minimum (negative means funding gap)
        min_cash = min_levered
        # Keep net cumulative for backward compat check but peak is levered
        cumulative = [p.cumulative_cash_flow for p in periods]  # noqa: F841
        peak_debt = max(p.closing_debt for p in periods) if periods else 0
        peak_equity = sum(p.equity_injection for p in periods)  # total equity invested as peak

        # Health score
        score = 100
        health = "Healthy"
        # Deductions
        if margin < 20:
            score -= 20
        if margin < 15:
            score -= 20
        if margin < 10:
            score -= 20
            health = "Critical"
        if peak_funding > gdv_report * 0.4:
            score -= 15
        if returns.get("equity_irr") is not None and returns["equity_irr"] < a.hurdle_rate_annual_pct/100:
            score -= 20
            if health != "Critical":
                health = "Watch"
        if not recon["cash_reconciliation"]:
            score -= 10
        if not recon["debt_reconciliation"]:
            score -= 10
        score = max(0, min(100, score))
        if score >= 80:
            health = "Healthy"
        elif score >= 60:
            health = "Watch"
        elif score >= 40:
            health = "Watch"
        else:
            health = "Critical"

        # Dashboard
        dashboard = {
            "financial_health": health,
            "health_score": score,
            "gdv": gdv_report,
            "gdc": gdc,
            "profit": profit,
            "margin_pct": margin,
            "profit_on_cost_pct": profit_on_cost,
            "sales": {
                "total_units": total_units,
                "sold_units": sold_units,
                "remaining_units": total_units - sold_units,
                "sales_rate": sold_units/total_units*100 if total_units else 0,
            },
            "collections": {
                "total_collections": sum(p.collections for p in periods),
                "collection_rate": a.collections.collection_rate_pct,
            },
            "construction": {
                "budget": a.construction.budget,
                "total_cost": sum(p.construction_cost for p in periods),
                "peak_month": max(periods, key=lambda x: x.construction_cost).label if periods else None,
            },
            "cashflow": {
                "minimum_cash": min_cash,
                "peak_funding": peak_funding,
                "peak_debt": peak_debt,
                "peak_equity": peak_equity,
            },
            "returns": {
                "unlevered_irr": returns.get("unlevered_irr"),
                "levered_irr": returns.get("levered_irr"),
                "equity_irr": returns.get("equity_irr"),
                "unlevered_npv": returns.get("unlevered_npv"),
                "equity_npv": returns.get("equity_npv"),
                "mirr": returns.get("mirr"),
                "moic": returns.get("moic"),
            },
            "reconciliation": recon,
        }

        run_id = f"{a.project_code}-{a.assumption_hash()}-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
        result = ModelResult(
            assumptions=a,
            run_id=run_id,
            timestamp=datetime.datetime.now().isoformat(),
            periods=periods,
            gdv=gdv_report,
            gdc=gdc,
            profit=profit,
            margin_pct=margin,
            profit_on_cost_pct=profit_on_cost,
            total_units=total_units,
            sold_units=sold_units,
            remaining_units=total_units - sold_units,
            unlevered_cash_flows=returns["unlevered_cash_flows"],
            levered_cash_flows=returns["levered_cash_flows"],
            equity_cash_flows=returns["equity_cash_flows"],
            unlevered_irr=returns["unlevered_irr"],
            levered_irr=returns["levered_irr"],
            equity_irr=returns["equity_irr"],
            unlevered_npv=returns["unlevered_npv"],
            levered_npv=returns["levered_npv"],
            equity_npv=returns["equity_npv"],
            mirr=returns["mirr"],
            moic=returns["moic"],
            equity_multiple=returns["moic"],
            payback_period=returns["payback_period"],
            peak_funding=peak_funding,
            peak_equity=peak_equity,
            peak_debt=peak_debt,
            minimum_cash=min_cash,
            funding_gap=peak_funding,
            reconciliation=recon,
            financial_health=health,
            health_score=score,
            dashboard=dashboard,
        )
        return result
