"""models/cashflow.py — Cashflow alias V1.2"""
from ..integrated_model import MonthlyRow as CashFlowPeriod, ModelResult
from ..base_models import CashFlowPeriod as BaseCashFlowPeriod
__all__ = ["CashFlowPeriod", "ModelResult", "BaseCashFlowPeriod"]
