"""
financial_statements.py — Income Statement, Balance Sheet, Cash Flow Analysis + Ratios
"""

from typing import Optional, Dict, List


def analyze_income_statement(
    revenue: Optional[float],
    cogs: Optional[float],
    opex: Optional[float] = 0,
    depreciation: Optional[float] = 0,
    amortization: Optional[float] = 0,
    interest: Optional[float] = 0,
    tax: Optional[float] = 0,
    other_income: Optional[float] = 0,
) -> Dict:
    if revenue is None:
        return {"error": "Revenue missing — cannot analyze income statement"}
    cogs = cogs or 0
    opex = opex or 0
    depreciation = depreciation or 0
    amortization = amortization or 0
    interest = interest or 0
    tax = tax or 0
    other_income = other_income or 0

    gross_profit = revenue - cogs
    gross_margin = (gross_profit / revenue * 100) if revenue != 0 else None
    operating_profit = gross_profit - opex + other_income
    ebitda = operating_profit + depreciation + amortization
    ebitda_margin = (ebitda / revenue * 100) if revenue != 0 else None
    ebit = ebitda - depreciation - amortization
    ebit_margin = (ebit / revenue * 100) if revenue != 0 else None
    ebt = ebit - interest
    net_income = ebt - tax
    net_margin = (net_income / revenue * 100) if revenue != 0 else None

    return {
        "revenue": revenue,
        "cogs": cogs,
        "gross_profit": gross_profit,
        "gross_margin_pct": gross_margin,
        "opex": opex,
        "operating_profit": operating_profit,
        "ebitda": ebitda,
        "ebitda_margin_pct": ebitda_margin,
        "ebit": ebit,
        "ebit_margin_pct": ebit_margin,
        "interest": interest,
        "ebt": ebt,
        "tax": tax,
        "net_income": net_income,
        "net_margin_pct": net_margin,
    }


def analyze_balance_sheet(
    cash: Optional[float] = 0,
    receivables: Optional[float] = 0,
    inventory: Optional[float] = 0,
    other_current_assets: Optional[float] = 0,
    ppe: Optional[float] = 0,
    payables: Optional[float] = 0,
    short_term_debt: Optional[float] = 0,
    other_current_liab: Optional[float] = 0,
    long_term_debt: Optional[float] = 0,
    equity: Optional[float] = 0,
) -> Dict:
    cash = cash or 0
    receivables = receivables or 0
    inventory = inventory or 0
    other_current_assets = other_current_assets or 0
    ppe = ppe or 0
    payables = payables or 0
    short_term_debt = short_term_debt or 0
    other_current_liab = other_current_liab or 0
    long_term_debt = long_term_debt or 0
    equity = equity or 0

    current_assets = cash + receivables + inventory + other_current_assets
    total_assets = current_assets + ppe
    current_liab = payables + short_term_debt + other_current_liab
    total_debt = short_term_debt + long_term_debt
    total_liab = current_liab + long_term_debt
    # Check balance: Assets = Liab + Equity (approx)
    balance_check = total_assets - (total_liab + equity)
    working_capital = current_assets - current_liab
    net_debt = total_debt - cash

    return {
        "cash": cash,
        "receivables": receivables,
        "inventory": inventory,
        "current_assets": current_assets,
        "ppe": ppe,
        "total_assets": total_assets,
        "payables": payables,
        "current_liab": current_liab,
        "total_debt": total_debt,
        "total_liab": total_liab,
        "equity": equity,
        "balance_check": balance_check,
        "working_capital": working_capital,
        "net_debt": net_debt,
        "current_assets_breakdown": {
            "cash": cash, "receivables": receivables, "inventory": inventory, "other": other_current_assets
        },
    }


def analyze_cash_flow(
    cfo: Optional[float] = 0,
    cfi: Optional[float] = 0,
    cff: Optional[float] = 0,
    capex: Optional[float] = 0,
) -> Dict:
    cfo = cfo or 0
    cfi = cfi or 0
    cff = cff or 0
    capex = capex or 0
    free_cash_flow = cfo - abs(capex)  # FCF = CFO - Capex
    # If CFI already includes capex, alternative: FCF = CFO + CFI (if CFI negative)
    net_change = cfo + cfi + cff
    return {
        "cfo": cfo,
        "cfi": cfi,
        "cff": cff,
        "capex": capex,
        "free_cash_flow": free_cash_flow,
        "net_change_in_cash": net_change,
    }


def calculate_ratios(
    income: Dict,
    balance: Dict,
    cashflow: Optional[Dict] = None,
) -> Dict:
    revenue = income.get("revenue")
    ebitda = income.get("ebitda")
    ebit = income.get("ebit")
    interest = income.get("interest")
    net_income = income.get("net_income")

    current_assets = balance.get("current_assets")
    current_liab = balance.get("current_liab")
    inventory = balance.get("inventory")
    receivables = balance.get("receivables")
    payables = balance.get("payables")
    total_debt = balance.get("total_debt")
    net_debt = balance.get("net_debt")
    equity = balance.get("equity")
    cash = balance.get("cash")

    # Liquidity
    current_ratio = (current_assets / current_liab) if current_liab else None
    quick_ratio = ((current_assets - inventory) / current_liab) if current_liab else None
    cash_ratio = (cash / current_liab) if current_liab else None

    # Leverage
    debt_to_equity = (total_debt / equity) if equity else None
    net_debt_to_ebitda = (net_debt / ebitda) if ebitda else None
    interest_coverage = (ebit / interest) if interest else None
    debt_ratio = (balance.get("total_liab", 0) / balance.get("total_assets", 1)) if balance.get("total_assets") else None

    # Efficiency (annualize if needed; here simple)
    # AR Days = Receivables / Revenue * 365
    ar_days = (receivables / revenue * 365) if revenue and receivables is not None else None
    ap_days = (payables / (income.get("cogs") or 1) * 365) if payables is not None and income.get("cogs") else None
    inventory_days = (inventory / (income.get("cogs") or 1) * 365) if inventory is not None and income.get("cogs") else None
    ccc = None
    if ar_days is not None and inventory_days is not None and ap_days is not None:
        ccc = ar_days + inventory_days - ap_days

    # Profitability
    roe = (net_income / equity * 100) if equity and net_income is not None else None
    roa = (net_income / balance.get("total_assets") * 100) if balance.get("total_assets") and net_income is not None else None

    # Working Capital
    wc = balance.get("working_capital")

    return {
        "current_ratio": current_ratio,
        "quick_ratio": quick_ratio,
        "cash_ratio": cash_ratio,
        "debt_to_equity": debt_to_equity,
        "net_debt_to_ebitda": net_debt_to_ebitda,
        "interest_coverage": interest_coverage,
        "debt_ratio": debt_ratio,
        "ar_days": ar_days,
        "ap_days": ap_days,
        "inventory_days": inventory_days,
        "cash_conversion_cycle_days": ccc,
        "roe_pct": roe,
        "roa_pct": roa,
        "working_capital": wc,
    }
