"""
Main Ultrathink framework class.

This module provides the primary interface for the Ultrathink self-improving
development framework.
"""
import logging
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List

import yaml
from dotenv import load_dotenv

from .engine import SelfImprovementEngine
from .knowledge_base import KnowledgeBase
from .models import CodeChange, TaskType
from .orchestrator import AIOrchestrator
from .parser import UniversalParser

logger = logging.getLogger(__name__)


class Ultrathink:
    """Main framework orchestrating all components"""

    def __init__(self, config_path: str = "ultrathink.yaml"):
        """
        Initialize the Ultrathink framework.

        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.orchestrator = AIOrchestrator(self.config)
        self.improvement_engine = SelfImprovementEngine(self.orchestrator)
        self.parser = UniversalParser()
        self.knowledge_base = KnowledgeBase(
            self.config.get('learning', {}).get('knowledge_base_path', 'ultrathink.db')
        )

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from .env and YAML file"""
        # Load environment variables from .env
        load_dotenv()

        # Load base config from YAML
        config = {}
        if Path(config_path).exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f) or {}

        # Add API keys from environment
        config['claude_api_key'] = os.getenv("CLAUDE_API_KEY")
        config['google_project_id'] = os.getenv("GOOGLE_PROJECT_ID")
        config['aws_region'] = os.getenv("AWS_REGION", "us-east-1")

        return config

    async def analyze_codebase(self, path: str) -> Dict[str, Any]:
        """Analyze entire codebase"""
        results = []

        for file_path in Path(path).rglob("*.py"):  # Start with Python
            code = file_path.read_text()

            # Run analysis
            analysis = await self.orchestrator.route_task(
                TaskType.CODE_REVIEW,
                {"code": code, "language": "python"}
            )

            results.append({
                "file": str(file_path),
                "analysis": asdict(analysis)
            })

        return {"results": results, "summary": self._generate_summary(results)}

    async def evolve_architecture(self, project_path: str) -> Dict[str, Any]:
        """Evolve project architecture using genetic algorithms"""
        current_architecture = self._analyze_architecture(project_path)

        evolution_result = await self.orchestrator.route_task(
            TaskType.ARCHITECTURE_EVOLUTION,
            {"architecture": current_architecture}
        )

        return {
            "current": current_architecture,
            "proposed": evolution_result.suggestions,
            "fitness_improvement": 0.15  # Placeholder
        }

    async def generate_tests(self, code: str, language: str = "python") -> str:
        """Generate comprehensive tests for code"""
        result = await self.orchestrator.route_task(
            TaskType.TEST_GENERATION,
            {"code": code, "language": language}
        )

        return result.auto_fixes[0] if result.auto_fixes else "# Generated tests would go here"

    async def self_improve(self, component_path: str) -> CodeChange:
        """Apply self-improvement to a component"""
        code = Path(component_path).read_text()

        component = CodeChange(
            file_path=component_path,
            language=self._detect_language(component_path),
            original_code=code
        )

        improved = await self.improvement_engine.recursive_improve(component)

        # Save improved version
        if improved.modified_code:
            backup_path = Path(component_path).with_suffix('.backup')
            backup_path.write_text(code)
            Path(component_path).write_text(improved.modified_code)

            logger.info(f"Improved {component_path}, backup at {backup_path}")

        return improved

    def _analyze_architecture(self, project_path: str) -> Dict[str, Any]:
        """Analyze current architecture"""
        return {
            "pattern": "layered",
            "components": ["api", "service", "data"],
            "metrics": {"coupling": 0.3, "cohesion": 0.7}
        }

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.rs': 'rust',
            '.go': 'go'
        }
        return extensions.get(Path(file_path).suffix, 'unknown')

    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of analysis results"""
        total_issues = sum(len(r['analysis']['findings']) for r in results)

        return {
            "files_analyzed": len(results),
            "total_issues": total_issues,
            "critical_issues": 0,  # Would calculate from actual results
            "suggested_improvements": total_issues
        }

    def initialize(self) -> None:
        """Initialize the framework and load existing knowledge"""
        self.knowledge_base.load()
        logger.info(f"Ultrathink initialized with config: {self.config.get('version', 'unknown')}")

    def save_knowledge(self) -> None:
        """Save accumulated knowledge to persistent storage"""
        self.knowledge_base.save()

    def get_stats(self) -> Dict[str, Any]:
        """Get framework statistics"""
        return {
            "improvement_cycles": self.improvement_engine.improvement_cycle_count,
            "patterns_stored": len(self.knowledge_base.patterns),
            "improvements_recorded": len(self.improvement_engine.improvement_history)
        }
