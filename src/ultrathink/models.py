"""
Data models for Ultrathink.

This module contains all the data classes and type definitions used throughout
the Ultrathink framework.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Any


class TaskType(Enum):
    """Types of tasks that can be performed by the system."""
    ANALYSIS = "analysis"
    REFACTOR = "refactor"
    TEST = "test"
    OPTIMIZE = "optimize"
    DEBUG = "debug"


@dataclass
class AIModel:
    """Represents an AI model configuration."""
    name: str
    provider: str
    capabilities: List[str]
    max_tokens: int = 4096
    temperature: float = 0.7


@dataclass
class CodeChange:
    """Represents a change to be made in code."""
    file_path: str
    line_number: int
    change_type: str  # add, modify, delete
    old_content: Optional[str] = None
    new_content: Optional[str] = None
    reason: str = ""


@dataclass
class AnalysisResult:
    """Result of code analysis."""
    task_id: str
    task_type: TaskType
    findings: List[str]
    suggestions: List[str]
    confidence: float
    metadata: Dict[str, Any]


@dataclass
class ImprovementHypothesis:
    """Represents a hypothesis for system improvement."""
    hypothesis_id: str
    description: str
    expected_benefit: str
    proposed_changes: List[CodeChange]
    priority: int
    validation_criteria: List[str]
