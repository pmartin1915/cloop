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

    async def analyze_codebase(self, path: str, save_findings: bool = True) -> Dict[str, Any]:
        """
        Analyze entire codebase.

        Args:
            path: Path to codebase directory
            save_findings: Whether to save findings to knowledge base

        Returns:
            Analysis results with summary
        """
        results = []

        for file_path in Path(path).rglob("*.py"):  # Start with Python
            try:
                code = file_path.read_text(encoding='utf-8')

                # Parse the code first
                parse_result = self.parser.parse(code, language="python")

                # Run AI analysis with parse metadata
                analysis = await self.orchestrator.route_task(
                    TaskType.CODE_REVIEW,
                    {
                        "code": code,
                        "language": "python",
                        "parse_metadata": parse_result
                    }
                )

                # Store findings in knowledge base if requested
                if save_findings and analysis.findings:
                    self.knowledge_base.store_analysis_findings(
                        file_path=str(file_path),
                        findings=analysis.findings,
                        parse_info=parse_result
                    )

                results.append({
                    "file": str(file_path),
                    "parse_info": parse_result,
                    "analysis": asdict(analysis)
                })

                logger.info(f"Analyzed {file_path}: {len(analysis.findings)} findings")

            except Exception as e:
                logger.error(f"Failed to analyze {file_path}: {e}")
                results.append({
                    "file": str(file_path),
                    "error": str(e)
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
        total_issues = 0
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        category_counts = {}

        for r in results:
            if 'analysis' in r and 'findings' in r['analysis']:
                findings = r['analysis']['findings']
                total_issues += len(findings)

                for finding in findings:
                    # Count by severity
                    severity = finding.get('severity', 'info')
                    if severity in severity_counts:
                        severity_counts[severity] += 1

                    # Count by category
                    category = finding.get('category', 'unknown')
                    category_counts[category] = category_counts.get(category, 0) + 1

        return {
            "files_analyzed": len(results),
            "files_with_errors": sum(1 for r in results if 'error' in r),
            "total_issues": total_issues,
            "severity_breakdown": severity_counts,
            "category_breakdown": category_counts,
            "critical_issues": severity_counts["critical"],
            "high_priority_issues": severity_counts["high"],
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
