# Financing — Single Source

LTC = debt / total_cost, LTV = debt / GDV.
Debt draw = min(total_cost*debt_pct/100, max(0, total_cost - collections)) via FinancingEngine.debt_draw_for_gap().
Monthly interest = opening_debt * annual_rate/100/12 (nominal) via FinancingEngine.monthly_interest().
Reconciliation per period: opening + draw + (interest if capitalized else 0) - repayment == closing (pytest.approx tol 0.01) via debt_reconciliation_check().
Integrated Model is single source → FinancingEngine → Debt Schedule.
