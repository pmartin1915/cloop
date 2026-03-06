"""
Ultrathink - Self-Improving Development Framework

A framework for AI-assisted software development with self-improvement capabilities.
"""

from .engine import SelfImprovementEngine
from .framework import Ultrathink
from .knowledge_base import KnowledgeBase
from .models import AIModel, AnalysisResult, CodeChange, ImprovementHypothesis, TaskType
from .orchestrator import AIOrchestrator
from .parser import UniversalParser

__version__ = "0.1.0"

__all__ = [
    "Ultrathink",
    "AIModel",
    "TaskType",
    "CodeChange",
    "AnalysisResult",
    "ImprovementHypothesis",
    "SelfImprovementEngine",
    "AIOrchestrator",
    "UniversalParser",
    "KnowledgeBase",
]
