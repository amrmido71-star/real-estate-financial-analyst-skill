"""models/project.py — Project model alias for Integrated Model V1.2"""
from ..base_models import Project
# Re-export ProjectAssumptions as canonical
from .assumptions import ProjectAssumptions
__all__ = ["Project", "ProjectAssumptions"]
