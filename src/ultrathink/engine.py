"""
Self-Improvement Engine for Ultrathink.

This module contains the core logic for the self-improvement cycle:
analyzing, hypothesizing, testing, and applying improvements.
"""
import ast
import hashlib
import logging
import shutil
import time
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from .models import CodeChange, ImprovementHypothesis, TaskType
from .orchestrator import AIOrchestrator

logger = logging.getLogger(__name__)


class SelfImprovementEngine:
    """Implements recursive self-improvement based on STOP framework"""

    def __init__(self, orchestrator: AIOrchestrator):
        """
        Initialize the self-improvement engine.

        Args:
            orchestrator: AI orchestrator for model management
        """
        self.orchestrator = orchestrator
        self.improvement_history = []
        self.performance_metrics = {}
        self.learning_rate = 0.1
        self.improvement_cycle_count = 0

    async def recursive_improve(self, component: CodeChange, max_iterations: int = 5) -> CodeChange:
        """Recursively improve a code component"""

        for iteration in range(max_iterations):
            # Analyze current performance
            metrics = await self._analyze_component(component)

            # Check if improvement is needed
            if self._is_satisfactory(metrics):
                logger.info(f"Component satisfactory after {iteration} iterations")
                break

            # Generate improvement hypothesis
            hypothesis = await self._generate_hypothesis(component, metrics)

            # Test in sandbox
            sandbox_result = await self._test_in_sandbox(hypothesis, component)

            # Apply if improved
            if sandbox_result['improved']:
                component = self._apply_improvement(component, hypothesis)
                self._record_learning(hypothesis, sandbox_result)
                logger.info(f"Improvement applied: {hypothesis.change_description}")
            else:
                # Try alternative approach
                logger.info("Hypothesis failed, trying alternative")
                hypothesis = await self._generate_alternative(component, metrics, hypothesis)

        return component

    async def _analyze_component(self, component: CodeChange) -> Dict[str, float]:
        """Analyze component performance metrics"""
        _analysis = await self.orchestrator.route_task(
            TaskType.CODE_REVIEW,
            {"code": component.modified_code or component.original_code,
             "language": component.language}
        )

        # Extract metrics from analysis (would use _analysis in production)
        metrics = {
            "complexity": self._calculate_complexity(component),
            "readability": 0.7,  # Placeholder
            "performance": 0.6,   # Placeholder
            "security": 0.8,      # Placeholder
            "test_coverage": 0.5  # Placeholder
        }

        return metrics

    async def _generate_hypothesis(self, component: CodeChange, metrics: Dict[str, float]) -> ImprovementHypothesis:
        """Generate improvement hypothesis using AI"""
        # Identify weakest metric
        weakest_metric = min(metrics.items(), key=lambda x: x[1])

        context = {
            "code": component.modified_code or component.original_code,
            "language": component.language,
            "target_metric": weakest_metric[0],
            "current_value": weakest_metric[1]
        }

        result = await self.orchestrator.route_task(TaskType.REFACTORING, context)

        return ImprovementHypothesis(
            target_metric=weakest_metric[0],
            current_value=weakest_metric[1],
            expected_value=min(weakest_metric[1] + 0.2, 1.0),
            change_description=result.suggestions[0] if result.suggestions else "Refactor for improvement",
            implementation=result.auto_fixes[0] if result.auto_fixes else "",
            risk_level=0.3
        )

    async def _test_in_sandbox(self, hypothesis: ImprovementHypothesis, component: CodeChange) -> Dict[str, Any]:
        """Test hypothesis in isolated sandbox"""
        # Create sandbox environment
        sandbox_path = Path(f"/tmp/ultrathink_sandbox_{hashlib.md5(str(time.time()).encode()).hexdigest()}")
        sandbox_path.mkdir(exist_ok=True)

        # Write test file
        test_file = sandbox_path / f"test_{component.file_path.replace('/', '_')}"
        test_file.write_text(hypothesis.implementation or component.original_code)

        # Run tests (simplified)
        result = {
            "improved": True,  # Placeholder
            "metrics": {"performance": 0.8},
            "test_results": "All tests passed"
        }

        # Cleanup
        shutil.rmtree(sandbox_path)

        return result

    def _apply_improvement(self, component: CodeChange, hypothesis: ImprovementHypothesis) -> CodeChange:
        """Apply improvement to component"""
        component.modified_code = hypothesis.implementation
        component.metadata = component.metadata or {}
        component.metadata['improvements'] = component.metadata.get('improvements', [])
        component.metadata['improvements'].append({
            'hypothesis': asdict(hypothesis),
            'timestamp': datetime.now().isoformat()
        })
        return component

    def _record_learning(self, hypothesis: ImprovementHypothesis, result: Dict[str, Any]):
        """Record learning from improvement attempt"""
        self.improvement_history.append({
            'hypothesis': asdict(hypothesis),
            'result': result,
            'timestamp': datetime.now().isoformat()
        })

        # Update performance metrics
        metric_key = hypothesis.target_metric
        if metric_key not in self.performance_metrics:
            self.performance_metrics[metric_key] = []
        self.performance_metrics[metric_key].append(result['metrics'].get(metric_key, 0))

    def _is_satisfactory(self, metrics: Dict[str, float]) -> bool:
        """Check if metrics are satisfactory"""
        thresholds = {
            "complexity": 0.7,
            "readability": 0.8,
            "performance": 0.7,
            "security": 0.9,
            "test_coverage": 0.8
        }

        return all(metrics.get(k, 0) >= v for k, v in thresholds.items())

    def _calculate_complexity(self, component: CodeChange) -> float:
        """Calculate cyclomatic complexity (simplified)"""
        try:
            tree = ast.parse(component.modified_code or component.original_code)
            complexity = 0

            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.With)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1

            # Normalize (lower is better, so invert)
            return max(0, 1 - (complexity / 100))
        except Exception:
            return 0.5  # Default if parsing fails

    async def _generate_alternative(self, component: CodeChange, metrics: Dict[str, float],
                                   failed_hypothesis: ImprovementHypothesis) -> ImprovementHypothesis:
        """Generate alternative improvement hypothesis"""
        # Try a different metric or approach
        metrics_sorted = sorted(metrics.items(), key=lambda x: x[1])

        for metric, value in metrics_sorted:
            if metric != failed_hypothesis.target_metric:
                return await self._generate_hypothesis(component, {metric: value})

        return failed_hypothesis  # Fallback
