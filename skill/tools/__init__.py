"""Real Estate Financial Analyst Skill — Tools Package v1.1"""

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

__all__ = [
    "calculate_gross_profit", "calculate_gross_margin", "calculate_operating_profit",
    "calculate_ebitda", "calculate_ebit", "calculate_net_profit", "calculate_net_margin",
    "calculate_variance", "calculate_variance_pct", "classify_variance", "calculate_roi",
    "calculate_gdv", "calculate_gdc", "calculate_development_profit", "calculate_development_margin",
    "calculate_npv", "calculate_npv_with_initial", "calculate_irr", "calculate_mirr",
    "detect_multiple_irr", "count_sign_changes", "irr_with_diagnostics",
    "calculate_peak_funding", "analyze_cashflow", "build_detailed_cashflow",
    "run_scenarios", "run_sensitivity_analysis", "run_two_way_sensitivity",
    "validate_financials", "validate_project", "calculate_data_quality_score",
    "build_collection_schedule", "calculate_sales_metrics", "build_aging_buckets",
    "generate_s_curve", "analyze_construction", "calculate_ltc", "calculate_ltv",
    "build_financing_schedule", "analyze_income_statement", "analyze_balance_sheet",
    "analyze_portfolio", "calculate_wacc", "dcf_valuation",
    "load_csv", "load_excel", "Unit", "Project",
]

__version__ = "1.1.0"
