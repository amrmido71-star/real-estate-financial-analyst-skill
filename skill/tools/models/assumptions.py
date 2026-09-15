"""
assumptions.py — Standardized ProjectAssumptions for Integrated Model V1.2
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from datetime import date


@dataclass
class LandAssumptions:
    area_sqm: float = 10000
    cost: float = 50_000_000
    acquisition_date: Optional[date] = None
    payment_schedule: Optional[List[Dict]] = None  # [{"date":date, "pct":50}, ...]
    transfer_fee_pct: float = 0.0


@dataclass
class ProductAssumptions:
    sellable_area_sqm: float = 50000
    bua_sqm: float = 65000
    far: Optional[float] = None
    unit_count: int = 100
    # Unit mix: list of {"type":str, "count":int, "area_sqm":float, "price_per_sqm":float, "price_per_unit":float}
    unit_mix: List[Dict] = field(default_factory=list)
    avg_price_per_sqm: float = 20000
    price_growth_annual_pct: float = 0.0
    price_lock_at_booking: bool = True


@dataclass
class SalesAssumptions:
    velocity_units_per_month: float = 8.0
    # Or custom monthly schedule: [5,8,10,...] — if provided, overrides velocity
    monthly_sales_schedule: Optional[List[int]] = None
    discount_pct: float = 0.0
    cancellation_rate_pct: float = 2.0
    sales_start_date: Optional[date] = None


@dataclass
class CollectionAssumptions:
    booking_pct: float = 10.0
    contract_pct: float = 10.0
    during_build_pct: float = 40.0
    handover_pct: float = 30.0
    post_handover_pct: float = 10.0
    # timing: months after sale for during_build, months after handover for post
    during_build_months: int = 12
    post_handover_months: int = 6
    collection_rate_pct: float = 90.0  # % of due collected as cash
    collection_lag_months: int = 0
    default_rate_pct: float = 1.0

    def total_pct(self) -> float:
        return self.booking_pct + self.contract_pct + self.during_build_pct + self.handover_pct + self.post_handover_pct

    def schedule(self) -> List[Dict]:
        # Returns installment schedule for collection engine
        return [
            {"label": "Booking", "pct": self.booking_pct, "months_after_sale": 0},
            {"label": "Contract", "pct": self.contract_pct, "months_after_sale": 1},
            {"label": "During Build", "pct": self.during_build_pct, "months_after_sale": self.during_build_months},
            {"label": "Handover", "pct": self.handover_pct, "anchor": "handover", "months_after_handover": 0},
            {"label": "Post Handover", "pct": self.post_handover_pct, "anchor": "handover", "months_after_handover": self.post_handover_months},
        ]


@dataclass
class ConstructionAssumptions:
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_months: int = 24
    budget: float = 200_000_000
    s_curve_type: Literal["linear","s_curve","front_loaded","back_loaded","custom"] = "s_curve"
    custom_curve: Optional[List[float]] = None  # monthly weights
    escalation_annual_pct: float = 0.0
    contingency_pct: float = 5.0
    contingency_included_in_gdc: bool = True  # if True, GDC includes contingency; else below base


@dataclass
class CostAssumptions:
    land: float = 0  # if 0, use land_assumptions.cost
    infrastructure: float = 0
    design: float = 0
    consultants: float = 0
    government_fees: float = 0
    marketing_pct_gdv: float = 2.5  # % of GDV
    commission_pct_gdv: float = 2.0
    overheads: float = 0
    taxes_pct: float = 0
    other: float = 0
    contingency_pct: float = 5.0


@dataclass
class FinancingAssumptions:
    debt_pct: float = 40.0  # % of GDC or funding gap
    equity_pct: float = 60.0
    interest_rate_annual_pct: float = 12.0
    commitment_fee_pct: float = 0.0
    arrangement_fee_pct: float = 0.0
    loan_start_month: int = 0
    repayment_start_month: Optional[int] = None  # if None, bullet at end
    tenor_months: Optional[int] = None
    repayment_type: Literal["bullet","amortizing","custom"] = "bullet"
    custom_repayment_schedule: Optional[List[float]] = None
    interest_payment_mode: Literal["cash","capitalized"] = "capitalized"
    ltc_based: bool = True
    target_ltc_pct: float = 60.0
    debt_yield_threshold: Optional[float] = None


@dataclass
class ProjectAssumptions:
    # Project
    project_name: str = "Untitled Project"
    project_code: str = "PRJ-001"
    start_date: date = field(default_factory=lambda: date(2027, 1, 1))
    end_date: date = field(default_factory=lambda: date(2030, 12, 31))
    currency: str = "EGP"
    discount_rate_annual_pct: float = 15.0
    hurdle_rate_annual_pct: float = 14.0
    tax_rate_pct: float = 22.5
    # Sub-assumptions
    land: LandAssumptions = field(default_factory=LandAssumptions)
    product: ProductAssumptions = field(default_factory=ProductAssumptions)
    sales: SalesAssumptions = field(default_factory=SalesAssumptions)
    collections: CollectionAssumptions = field(default_factory=CollectionAssumptions)
    construction: ConstructionAssumptions = field(default_factory=ConstructionAssumptions)
    costs: CostAssumptions = field(default_factory=CostAssumptions)
    financing: FinancingAssumptions = field(default_factory=FinancingAssumptions)

    def validate(self) -> List[str]:
        errors = []
        if self.product.sellable_area_sqm <= 0:
            errors.append("sellable_area_sqm must be >0")
        if self.financing.debt_pct + self.financing.equity_pct != 100:
            # Allow normalization, but warn
            if abs(self.financing.debt_pct + self.financing.equity_pct - 100) > 0.1:
                errors.append(f"debt_pct + equity_pct must =100, got {self.financing.debt_pct + self.financing.equity_pct}")
        if abs(self.collections.total_pct() - 100) > 0.01:
            errors.append(f"Collection schedule must sum to 100, got {self.collections.total_pct()}")
        if self.construction.duration_months <= 0:
            errors.append("construction duration must be >0")
        return errors

    def to_dict(self) -> Dict:
        # For audit trail / hashing
        d = {
            "project_name": self.project_name,
            "currency": self.currency,
            "discount_rate": self.discount_rate_annual_pct,
            "land_cost": self.land.cost,
            "sellable": self.product.sellable_area_sqm,
            "price_per_sqm": self.product.avg_price_per_sqm,
            "velocity": self.sales.velocity_units_per_month,
            "construction_budget": self.construction.budget,
            "debt_pct": self.financing.debt_pct,
            "interest": self.financing.interest_rate_annual_pct,
        }
        return d

    def assumption_hash(self) -> str:
        import hashlib
        import json
        s = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.md5(s.encode()).hexdigest()[:8]
