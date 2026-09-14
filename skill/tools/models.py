"""
models.py — Standard Data Models using dataclasses
Provides typed, validated structures for Project, Unit, Sale, Collection, etc.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Literal, Dict
from datetime import date


@dataclass
class Unit:
    unit_code: str
    unit_type: str
    area_sqm: float
    price_per_unit: float
    status: Literal["available", "reserved", "sold", "cancelled"] = "available"
    price_per_sqm: Optional[float] = None

    def __post_init__(self):
        if self.price_per_sqm is None and self.area_sqm and self.area_sqm != 0:
            self.price_per_sqm = self.price_per_unit / self.area_sqm

@dataclass
class CostItem:
    category: str  # land, construction, infrastructure, soft, marketing, financing, admin, contingency, fees
    amount: float
    period: Optional[int] = None  # month index
    notes: Optional[str] = None

@dataclass
class Sale:
    sale_id: str
    unit_code: str
    sale_date: date
    contracted_value: float
    status: Literal["booking", "contracted", "cancelled"] = "contracted"
    payment_plan: Optional[str] = None

@dataclass
class Collection:
    collection_id: str
    sale_id: str
    due_date: date
    due_amount: float
    collected_date: Optional[date] = None
    collected_amount: float = 0.0
    aging_bucket: Optional[str] = None

@dataclass
class InstallmentSchedule:
    """Defines payment plan: e.g., booking 10%, contract 10%, during_build 40%, handover 30%, post 10%"""
    name: str
    installments: List[Dict]  # [{"label": "Booking", "pct": 10, "timing": "on_sale"}, ...]
    total_pct: float = field(init=False)

    def __post_init__(self):
        self.total_pct = sum(i.get("pct", 0) for i in self.installments)
        if abs(self.total_pct - 100) > 0.01:
            raise ValueError(f"Installment schedule must sum to 100%, got {self.total_pct}%")

@dataclass
class Project:
    project_code: str
    name: str
    project_type: Literal["residential", "commercial", "mixed_use", "hospitality", "land"]
    sellable_area_sqm: float
    bua_sqm: float
    units: List[Unit] = field(default_factory=list)
    costs: List[CostItem] = field(default_factory=list)
    sales: List[Sale] = field(default_factory=list)
    collections: List[Collection] = field(default_factory=list)
    start_date: Optional[date] = None
    delivery_date: Optional[date] = None
    currency: str = "EGP"

    @property
    def total_units(self) -> int:
        return len(self.units)

    @property
    def sold_units(self) -> int:
        return sum(1 for u in self.units if u.status == "sold")

    @property
    def gdv(self) -> float:
        return sum(u.price_per_unit for u in self.units)

    @property
    def gdc(self) -> float:
        return sum(c.amount for c in self.costs)

@dataclass
class CashFlowPeriod:
    period: int  # 0,1,2...
    label: str  # e.g., "2025-01"
    inflows_collections: float = 0.0
    inflows_financing: float = 0.0
    outflows_construction: float = 0.0
    outflows_soft: float = 0.0
    outflows_financing: float = 0.0
    outflows_other: float = 0.0

    @property
    def total_inflows(self) -> float:
        return self.inflows_collections + self.inflows_financing

    @property
    def total_outflows(self) -> float:
        return self.outflows_construction + self.outflows_soft + self.outflows_financing + self.outflows_other

    @property
    def net(self) -> float:
        return self.total_inflows - self.total_outflows

@dataclass
class FinancialStatement:
    period: str
    revenue: Optional[float] = None
    cogs: Optional[float] = None
    gross_profit: Optional[float] = None
    opex: Optional[float] = None
    ebitda: Optional[float] = None
    ebit: Optional[float] = None
    interest: Optional[float] = None
    tax: Optional[float] = None
    net_income: Optional[float] = None
    cash: Optional[float] = None
    receivables: Optional[float] = None
    inventory: Optional[float] = None
    payables: Optional[float] = None
    debt: Optional[float] = None
    equity: Optional[float] = None

@dataclass
class ScenarioAssumptions:
    selling_price_change_pct: float = 0.0
    construction_cost_change_pct: float = 0.0
    soft_cost_change_pct: float = 0.0
    land_cost_change_pct: float = 0.0
    marketing_cost_change_pct: float = 0.0
    financing_cost_change_pct: float = 0.0
    sales_velocity_change_pct: float = 0.0  # negative = slower
    collection_rate_change_pct: float = 0.0
    interest_rate_change_pct: float = 0.0  # absolute pts? we use pct of rate
    delay_months: int = 0

@dataclass
class ScenarioResult:
    name: str  # Base, Best, Worst
    assumptions: ScenarioAssumptions
    gdv: Optional[float] = None
    gdc: Optional[float] = None
    profit: Optional[float] = None
    margin_pct: Optional[float] = None
    irr: Optional[float] = None
    npv: Optional[float] = None
    equity_irr: Optional[float] = None
    peak_funding: Optional[float] = None
    cash_flows: Optional[List[float]] = None

@dataclass
class DataQualityReport:
    score: int  # 0-100
    critical_errors: int
    warnings: int
    missing_fields: int
    details: Dict[str, List[str]]
    confidence: Literal["High", "Medium", "Low"]
