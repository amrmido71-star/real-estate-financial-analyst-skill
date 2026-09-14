"""Real Estate Financial Analyst Skill — Tools Package"""

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
)

from .investment_metrics import (
    calculate_npv,
    calculate_irr,
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
)

from .scenario_analysis import (
    run_scenarios,
    run_sensitivity_analysis,
)

from .data_validation import (
    validate_financials,
    validate_project,
    validate_cashflow,
)

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
    "calculate_npv",
    "calculate_irr",
    "calculate_equity_multiple",
    "calculate_cash_on_cash",
    "calculate_payback_period",
    "calculate_roic",
    "calculate_cumulative_cashflow",
    "calculate_peak_funding",
    "calculate_dscr",
    "analyze_cashflow",
    "run_scenarios",
    "run_sensitivity_analysis",
    "validate_financials",
    "validate_project",
    "validate_cashflow",
]

__version__ = "1.0.0"
