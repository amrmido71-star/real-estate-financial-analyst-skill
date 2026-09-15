"""Real Estate Financial Analyst Skill — Tools Package v1.2.1 — Integrated Development Model"""

from .financial_calculations import (
    calculate_gross_profit,
    calculate_gross_margin,
    calculate_operating_profit,
    calculate_ebitda,
    calculate_ebit,
    calculate_net_profit,
    calculate_net_margin,
    calculate_variance,
    calculate_variance_pct,
    classify_variance,
    calculate_roi,
    calculate_break_even_sales,
)

from .project_metrics import (
    calculate_gdv,
    calculate_gdc,
    calculate_development_profit,
    calculate_development_margin,
    calculate_margin_on_cost,
    calculate_cost_per_sqm,
    calculate_price_per_sqm,
    calculate_profit_per_sqm,
    calculate_land_cost_pct,
    calculate_construction_cost_pct,
    calculate_break_even_pct,
    calculate_break_even_price,
    calculate_break_even_revenue,
    calculate_break_even_units,
    calculate_safety_margin,
)

from .investment_metrics import (
    calculate_npv,
    calculate_npv_with_initial,
    calculate_irr,
    calculate_mirr,
    detect_multiple_irr,
    count_sign_changes,
    irr_with_diagnostics,
    calculate_equity_multiple,
    calculate_cash_on_cash,
    calculate_payback_period,
    calculate_roic,
)

from .cashflow_analysis import (
    calculate_cumulative_cashflow,
    calculate_peak_funding,
    calculate_dscr,
    analyze_cashflow,
    build_detailed_cashflow,
    aggregate_to_quarterly,
    aggregate_to_annual,
)

from .scenario_analysis import (
    run_scenarios,
    run_sensitivity_analysis,
    run_two_way_sensitivity,
    tornado_sensitivity,
    format_scenario_table,
)

from .data_validation import (
    validate_financials,
    validate_project,
    validate_cashflow,
    validate_sales_report,
    validate_transactions,
    calculate_data_quality_score,
    assess_confidence,
)

# New engines
from .sales_collection import (
    build_collection_schedule,
    aggregate_monthly_cash,
    calculate_sales_metrics,
    calculate_collection_metrics_detailed,
    build_aging_buckets,
    calculate_aging_summary,
    calculate_sales_velocity,
)

from .construction_analysis import (
    calculate_eac,
    calculate_etc,
    generate_s_curve,
    analyze_construction,
    monthly_progress_report,
)

from .financing import (
    calculate_ltc,
    calculate_ltv,
    build_financing_schedule,
    calculate_dscr_series,
    calculate_facility_headroom,
    levered_vs_unlevered,
)

from .financial_statements import (
    analyze_income_statement,
    analyze_balance_sheet,
    analyze_cash_flow,
    calculate_ratios,
)

from .portfolio_analysis import analyze_portfolio

from .valuation import (
    calculate_wacc,
    calculate_cost_of_equity_capm,
    dcf_valuation,
    residual_land_value,
    comparable_valuation,
    income_valuation,
)

from .data_loader import load_csv, load_excel, normalize_columns, validate_schema, df_to_records

from .models import (
    Unit, CostItem, Sale, Collection, Project, CashFlowPeriod, FinancialStatement,
    ScenarioAssumptions, ScenarioResult, DataQualityReport
)

from .exceptions import (
    FinancialSkillError, InvalidDiscountRateError, InvalidProjectDataError,
    MissingRequiredFieldError, InconsistentFinancialDataError, InvalidCashFlowError,
    MultipleIRRError, NoIRRError
)


# V1.2 Integrated Development Model — Central Orchestrator
from .models.assumptions import (
    ProjectAssumptions, LandAssumptions, ProductAssumptions,
    SalesAssumptions, CollectionAssumptions, ConstructionAssumptions,
    CostAssumptions, FinancingAssumptions,
)
from .integrated_model import IntegratedRealEstateModel, ModelResult, MonthlyRow
from .model_runner import ModelRunner
from .model_validation import validate_reconciliation, audit_trail
from .reporting import build_dashboard, build_executive_summary, build_management_pack
from .exceptions import (
    ModelValidationError, InconsistentTimelineError, FundingShortfallError,
    InvalidCapitalStructureError, InvalidScenarioError, ReconciliationError,
)

# V1.2 Engines
from .engines.revenue_engine import RevenueEngine
from .engines.sales_engine import SalesEngine
from .engines.collection_engine import CollectionEngine
from .engines.construction_engine import ConstructionEngine
from .engines.financing_engine import FinancingEngine
from .engines.cashflow_engine import CashflowEngine
from .engines.return_engine import ReturnEngine
from .engines.scenario_engine import ScenarioEngine

__all__ = [
    "calculate_gross_profit",
    "calculate_gross_margin",
    "calculate_operating_profit",
    "calculate_ebitda",
    "calculate_ebit",
    "calculate_net_profit",
    "calculate_net_margin",
    "calculate_variance",
    "calculate_variance_pct",
    "classify_variance",
    "calculate_roi",
    "calculate_break_even_sales",
    "calculate_gdv",
    "calculate_gdc",
    "calculate_development_profit",
    "calculate_development_margin",
    "calculate_margin_on_cost",
    "calculate_cost_per_sqm",
    "calculate_price_per_sqm",
    "calculate_profit_per_sqm",
    "calculate_land_cost_pct",
    "calculate_construction_cost_pct",
    "calculate_break_even_pct",
    "calculate_break_even_price",
    "calculate_break_even_revenue",
    "calculate_break_even_units",
    "calculate_safety_margin",
    "calculate_npv",
    "calculate_npv_with_initial",
    "calculate_irr",
    "calculate_mirr",
    "detect_multiple_irr",
    "count_sign_changes",
    "irr_with_diagnostics",
    "calculate_equity_multiple",
    "calculate_cash_on_cash",
    "calculate_payback_period",
    "calculate_roic",
    "calculate_cumulative_cashflow",
    "calculate_peak_funding",
    "calculate_dscr",
    "analyze_cashflow",
    "build_detailed_cashflow",
    "aggregate_to_quarterly",
    "aggregate_to_annual",
    "run_scenarios",
    "run_sensitivity_analysis",
    "run_two_way_sensitivity",
    "tornado_sensitivity",
    "format_scenario_table",
    "validate_financials",
    "validate_project",
    "validate_cashflow",
    "validate_sales_report",
    "validate_transactions",
    "calculate_data_quality_score",
    "assess_confidence",
    "build_collection_schedule",
    "aggregate_monthly_cash",
    "calculate_sales_metrics",
    "calculate_collection_metrics_detailed",
    "build_aging_buckets",
    "calculate_aging_summary",
    "calculate_sales_velocity",
    "calculate_eac",
    "calculate_etc",
    "generate_s_curve",
    "analyze_construction",
    "monthly_progress_report",
    "calculate_ltc",
    "calculate_ltv",
    "build_financing_schedule",
    "calculate_dscr_series",
    "calculate_facility_headroom",
    "levered_vs_unlevered",
    "analyze_income_statement",
    "analyze_balance_sheet",
    "analyze_cash_flow",
    "calculate_ratios",
    "calculate_wacc",
    "calculate_cost_of_equity_capm",
    "dcf_valuation",
    "residual_land_value",
    "comparable_valuation",
    "income_valuation",
    "Unit",
    "CostItem",
    "Sale",
    "Collection",
    "Project",
    "CashFlowPeriod",
    "FinancialStatement",
    "ScenarioAssumptions",
    "ScenarioResult",
    "DataQualityReport",
    "FinancialSkillError",
    "InvalidDiscountRateError",
    "InvalidProjectDataError",
    "MissingRequiredFieldError",
    "InconsistentFinancialDataError",
    "InvalidCashFlowError",
    "MultipleIRRError",
    "NoIRRError",
    "ProjectAssumptions",
    "LandAssumptions",
    "ProductAssumptions",
    "SalesAssumptions",
    "CollectionAssumptions",
    "ConstructionAssumptions",
    "CostAssumptions",
    "FinancingAssumptions",
    "ModelValidationError",
    "InconsistentTimelineError",
    "FundingShortfallError",
    "InvalidCapitalStructureError",
    "InvalidScenarioError",
    "ReconciliationError",
    "analyze_portfolio",
    "load_csv",
    "load_excel",
    "normalize_columns",
    "validate_schema",
    "df_to_records",
    "IntegratedRealEstateModel",
    "ModelResult",
    "MonthlyRow",
    "ModelRunner",
    "validate_reconciliation",
    "audit_trail",
    "build_dashboard",
    "build_executive_summary",
    "build_management_pack",
    "RevenueEngine",
    "SalesEngine",
    "CollectionEngine",
    "ConstructionEngine",
    "FinancingEngine",
    "CashflowEngine",
    "ReturnEngine",
    "ScenarioEngine",
]

__version__ = "1.2.1"
