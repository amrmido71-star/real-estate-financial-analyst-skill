"""
exceptions.py — Custom exceptions for Real Estate Financial Analyst Skill
"""

class FinancialSkillError(Exception):
    """Base exception for all skill errors"""
    pass

class InvalidDiscountRateError(FinancialSkillError):
    pass

class InvalidProjectDataError(FinancialSkillError):
    pass

class MissingRequiredFieldError(FinancialSkillError):
    def __init__(self, field: str, context: str = ""):
        msg = f"Missing required field: '{field}'"
        if context:
            msg += f" ({context})"
        super().__init__(msg)
        self.field = field

class InconsistentFinancialDataError(FinancialSkillError):
    pass

class InvalidCashFlowError(FinancialSkillError):
    pass

class MultipleIRRError(FinancialSkillError):
    def __init__(self, message: str, sign_changes: int):
        super().__init__(message)
        self.sign_changes = sign_changes

class NoIRRError(FinancialSkillError):
    pass

class InvalidAssumptionError(FinancialSkillError):
    pass
