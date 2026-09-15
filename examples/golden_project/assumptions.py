"""
assumptions.py — Golden Project Assumptions V1.2
Audited flagship project: East Cairo Compound — 300 units, New Capital, Egypt
This is the canonical Golden Case for regression testing.
All numbers are realistic and audited: GDV/GDC reconciles to ModelResult.
"""
from datetime import date
from skill.tools.models.assumptions import (
    ProjectAssumptions, LandAssumptions, ProductAssumptions,
    SalesAssumptions, CollectionAssumptions, ConstructionAssumptions,
    CostAssumptions, FinancingAssumptions
)

def golden_assumptions() -> ProjectAssumptions:
    """
    Golden Case: East Cairo — 300 units, mixed villas/apartments
    Start 2027-01-01, Handover mid-2029, Sell-out 36 months
    """
    return ProjectAssumptions(
        project_name="East Cairo Compound — Golden Case",
        project_code="GOLDEN-001",
        start_date=date(2027, 1, 1),
        end_date=date(2029, 12, 31),
        currency="EGP",
        discount_rate_annual_pct=14.0,
        hurdle_rate_annual_pct=18.0,
        tax_rate_pct=22.5,
        land=LandAssumptions(
            area_sqm=80000,
            cost=420_000_000,
            transfer_fee_pct=3.0,
        ),
        product=ProductAssumptions(
            sellable_area_sqm=85000,
            bua_sqm=110000,
            unit_count=300,
            avg_price_per_sqm=34000,
            price_growth_annual_pct=4.0,
            price_lock_at_booking=True,
            unit_mix=[],  # equal units, GDV = sellable * price = 2.89B
        ),
        sales=SalesAssumptions(
            velocity_units_per_month=9,
            discount_pct=2.0,
            cancellation_rate_pct=2.0,
        ),
        collections=CollectionAssumptions(
            booking_pct=10.0,
            contract_pct=10.0,
            during_build_pct=35.0,
            handover_pct=25.0,
            post_handover_pct=20.0,
            during_build_months=12,
            post_handover_months=6,
            collection_rate_pct=90.0,
            collection_lag_months=0,
            default_rate_pct=2.0,
        ),
        construction=ConstructionAssumptions(
            duration_months=28,
            budget=1_050_000_000,
            s_curve_type="s_curve",
            escalation_annual_pct=5.0,
            contingency_pct=5.0,
            contingency_included_in_gdc=True,
        ),
        costs=CostAssumptions(
            design=18_000_000,
            consultants=22_000_000,
            infrastructure=45_000_000,
            government_fees=12_000_000,
            marketing_pct_gdv=2.2,
            commission_pct_gdv=2.0,
            overheads=24_000_000,
            other=10_000_000,
            contingency_pct=5.0,
        ),
        financing=FinancingAssumptions(
            debt_pct=50.0,
            equity_pct=50.0,
            interest_rate_annual_pct=13.5,
            interest_payment_mode="capitalized",
            ltc_based=True,
            target_ltc_pct=55.0,
            repayment_type="bullet",
        ),
    )


def base_assumptions() -> ProjectAssumptions:
    """Alias for backward compat"""
    return golden_assumptions()

def best_case_delta():
    return {
        "selling_price_change_pct": 10,
        "construction_cost_change_pct": -5,
        "sales_velocity_change_pct": 20,
        "collection_rate_change_pct": 5,
        "interest_rate_delta": -1.5,
    }

def worst_case_delta():
    return {
        "selling_price_change_pct": -10,
        "construction_cost_change_pct": 15,
        "sales_velocity_change_pct": -25,
        "collection_rate_change_pct": -10,
        "interest_rate_delta": 2.0,
        "delay_months": 6,
    }

def stress_case_delta():
    return {
        "selling_price_change_pct": -15,
        "construction_cost_change_pct": 20,
        "collection_rate_change_pct": -15,
        "interest_rate_delta": 3.0,
        "delay_months": 9,
    }
