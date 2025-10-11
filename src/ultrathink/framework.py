"""
Main Ultrathink framework class.

This module provides the primary interface for the Ultrathink self-improving
development framework.
"""
from typing import Optional, List, Dict, Any
from pathlib import Path
from .orchestrator import AIOrchestrator
from .engine import SelfImprovementEngine
from .parser import UniversalParser
from .knowledge_base import KnowledgeBase
from .models import AIModel


class Ultrathink:
    """
    Main Ultrathink framework for self-improving development.

    This class provides the high-level interface for:
    - Code analysis and understanding
    - Self-improvement cycles
    - Knowledge management
    - AI-assisted development
    """

    def __init__(
        self,
        project_path: str,
        models: Optional[List[AIModel]] = None,
        knowledge_base_path: Optional[str] = None
    ):
        """
        Initialize the Ultrathink framework.

        Args:
            project_path: Root path of the project to work with
            models: List of AI models to use
            knowledge_base_path: Path to persistent knowledge storage
        """
        self.project_path = Path(project_path)
        self.orchestrator = AIOrchestrator(models)
        self.parser = UniversalParser()
        self.knowledge_base = KnowledgeBase(knowledge_base_path)
        self.engine = SelfImprovementEngine(
            self.orchestrator,
            self.knowledge_base,
            self.parser
        )

    def initialize(self) -> None:
        """Initialize the framework and load existing knowledge."""
        self.knowledge_base.load()
        print(f"Ultrathink initialized for project: {self.project_path}")

    def analyze(self, paths: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze code for improvement opportunities.

        Args:
            paths: Specific paths to analyze. If None, analyzes entire project.

        Returns:
            Analysis results summary
        """
        if paths is None:
            paths = [str(self.project_path)]

        result = self.engine.analyze_codebase(paths)
        return {
            "findings_count": len(result.findings),
            "suggestions_count": len(result.suggestions),
            "confidence": result.confidence
        }

    def improve(self, target_paths: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run a self-improvement cycle.

        Args:
            target_paths: Specific paths to improve. If None, uses entire project.

        Returns:
            Summary of improvements made
        """
        if target_paths is None:
            target_paths = [str(self.project_path)]

        return self.engine.run_improvement_cycle(target_paths)

    def save_knowledge(self) -> None:
        """Save accumulated knowledge to persistent storage."""
        self.knowledge_base.save()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get framework statistics.

        Returns:
            Dictionary with usage statistics
        """
        return {
            "improvement_cycles": self.engine.improvement_cycle_count,
            "hypotheses_stored": len(self.knowledge_base.hypotheses),
            "analyses_performed": len(self.knowledge_base.analysis_history),
            "project_path": str(self.project_path)
        }
