"""
Data models for Ultrathink.

This module contains all the data classes and type definitions used throughout
the Ultrathink framework.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class AIModel(Enum):
    """Available AI models for different tasks"""
    CLAUDE_OPUS = "claude-opus-4-1-20250805"
    GEMINI_ULTRA = "gemini-ultra"
    AWS_BEDROCK_CLAUDE = "anthropic.claude-v2"
    LOCAL_CODELLAMA = "codellama-13b"


class TaskType(Enum):
    """Types of development tasks"""
    CODE_REVIEW = "code_review"
    TEST_GENERATION = "test_generation"
    REFACTORING = "refactoring"
    SECURITY_ANALYSIS = "security_analysis"
    ARCHITECTURE_EVOLUTION = "architecture_evolution"
    BUG_FIXING = "bug_fixing"
    DOCUMENTATION = "documentation"


@dataclass
class CodeChange:
    """Represents a code change for analysis"""
    file_path: str
    language: str
    original_code: str
    modified_code: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AnalysisResult:
    """Result from AI analysis"""
    task_type: TaskType
    findings: List[Dict[str, Any]]
    suggestions: List[str]
    auto_fixes: Optional[List[str]] = None
    confidence: float = 0.0
    model_used: str = ""
    timestamp: str = ""


@dataclass
class ImprovementHypothesis:
    """Hypothesis for code improvement"""
    target_metric: str
    current_value: float
    expected_value: float
    change_description: str
    implementation: str
    risk_level: float
