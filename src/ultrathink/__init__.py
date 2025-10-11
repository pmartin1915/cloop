"""
Ultrathink - Self-Improving Development Framework

A framework for AI-assisted software development with self-improvement capabilities.
"""

from .framework import Ultrathink
from .models import (
    AIModel,
    TaskType,
    CodeChange,
    AnalysisResult,
    ImprovementHypothesis
)
from .engine import SelfImprovementEngine
from .orchestrator import AIOrchestrator
from .parser import UniversalParser
from .knowledge_base import KnowledgeBase

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
