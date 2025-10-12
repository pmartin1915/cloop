"""
Learning Engine for Ultrathink.

This module analyzes recurring code issues and generates patches to
prevent them from appearing in future code generation.
"""
import difflib
import hashlib
import json
import logging
from typing import Any, Dict, List

from .knowledge_base import KnowledgeBase

logger = logging.getLogger(__name__)


class LearningEngine:
    """
    Identifies patterns from analysis findings and generates improvement patches.

    The learning engine:
    1. Groups similar issues to identify patterns
    2. Generates actionable patches from patterns
    3. Stores learned improvements for future application
    """

    def __init__(self, knowledge_base: KnowledgeBase, similarity_threshold: float = 0.8):
        """
        Initialize the learning engine.

        Args:
            knowledge_base: KnowledgeBase instance for data access
            similarity_threshold: Threshold for grouping similar issues (0-1)
        """
        self.knowledge_base = knowledge_base
        self.similarity_threshold = similarity_threshold

    def learn_from_findings(self, occurrence_threshold: int = 2) -> Dict[str, Any]:
        """
        Analyze stored findings and generate improvement patches.

        Args:
            occurrence_threshold: Minimum occurrences to consider as pattern

        Returns:
            Learning summary with patterns and patches generated
        """
        logger.info(f"Starting learning process with threshold: {occurrence_threshold}")

        # Get recurring issues from knowledge base
        recurring_issues = self.knowledge_base.get_recurring_issues(threshold=occurrence_threshold)

        if not recurring_issues:
            logger.info("No recurring issues found")
            return {
                "patterns_identified": 0,
                "patches_generated": 0,
                "patterns": [],
                "patches": []
            }

        # Group similar issues into patterns
        patterns = self._identify_patterns(recurring_issues)

        # Generate patches for each pattern
        patches = []
        for pattern in patterns:
            generated_patches = self._generate_patches_for_pattern(pattern)
            patches.extend(generated_patches)

        # Store patches in knowledge base
        for patch in patches:
            self.knowledge_base.store_improvement(patch)

        logger.info(f"Learning complete: {len(patterns)} patterns, {len(patches)} patches")

        return {
            "patterns_identified": len(patterns),
            "patches_generated": len(patches),
            "patterns": patterns,
            "patches": patches
        }

    def _identify_patterns(self, recurring_issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Group similar recurring issues into patterns.

        Args:
            recurring_issues: List of recurring issues from knowledge base

        Returns:
            List of identified patterns
        """
        patterns = []

        # Group by category first
        by_category = {}
        for issue in recurring_issues:
            category = issue.get('category', 'unknown')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(issue)

        # Within each category, group similar descriptions
        for category, issues in by_category.items():
            grouped = self._group_similar_issues(issues)

            for group in grouped:
                pattern_id = hashlib.md5(
                    json.dumps({
                        'category': category,
                        'description': group[0]['description']
                    }).encode()
                ).hexdigest()

                pattern = {
                    'id': pattern_id,
                    'pattern_type': category,
                    'description': group[0]['description'],
                    'severity': group[0]['severity'],
                    'frequency': sum(issue['frequency'] for issue in group),
                    'affected_files': list(set(
                        file for issue in group
                        for file in issue.get('affected_files', [])
                    )),
                    'examples': group[:3]  # Keep top 3 examples
                }

                patterns.append(pattern)

                # Store pattern in knowledge base
                self.knowledge_base.store_pattern({
                    'pattern_type': category,
                    'description': pattern['description'],
                    'context': {
                        'severity': pattern['severity'],
                        'frequency': pattern['frequency']
                    }
                })

        logger.info(f"Identified {len(patterns)} patterns from {len(recurring_issues)} recurring issues")
        return patterns

    def _group_similar_issues(self, issues: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """
        Group issues with similar descriptions using fuzzy matching.

        Args:
            issues: List of issues to group

        Returns:
            List of issue groups
        """
        if not issues:
            return []

        groups = []
        used = set()

        for i, issue1 in enumerate(issues):
            if i in used:
                continue

            group = [issue1]
            used.add(i)

            for j, issue2 in enumerate(issues):
                if j in used or i == j:
                    continue

                similarity = self._calculate_similarity(
                    issue1['description'],
                    issue2['description']
                )

                if similarity >= self.similarity_threshold:
                    group.append(issue2)
                    used.add(j)

            groups.append(group)

        return groups

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two text strings.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score (0-1)
        """
        return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def _generate_patches_for_pattern(self, pattern: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate code patches to fix a pattern.

        Args:
            pattern: Pattern dictionary with description, category, severity

        Returns:
            List of patch dictionaries
        """
        patches = []

        category = pattern['pattern_type']
        description = pattern['description'].lower()

        # Pattern matching for common issues and their fixes
        patch_generators = {
            'bug': self._generate_bug_patches,
            'security': self._generate_security_patches,
            'quality': self._generate_quality_patches,
            'style': self._generate_style_patches,
            'performance': self._generate_performance_patches
        }

        generator = patch_generators.get(category, self._generate_generic_patch)
        generated = generator(pattern, description)

        for patch_data in generated:
            patch = {
                'pattern_id': pattern['id'],
                'template_file': patch_data.get('template_file', ''),
                'line_pattern': patch_data.get('line_pattern', ''),
                'replacement': patch_data.get('replacement', ''),
                'reason': patch_data.get('reason', pattern['description'])
            }
            patches.append(patch)

        return patches

    def _generate_bug_patches(self, pattern: Dict[str, Any], description: str) -> List[Dict[str, Any]]:
        """Generate patches for bug-related issues"""
        patches = []

        # Division by zero
        if 'division' in description and 'zero' in description:
            patches.append({
                'template_file': 'calculator.py',
                'line_pattern': r'def divide\(.*\):',
                'replacement': '''def divide(self, a: float, b: float) -> float:
        """Divide two numbers with zero check."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b''',
                'reason': 'Add zero division check to prevent runtime errors'
            })

        # Null/None checks
        if 'none' in description or 'null' in description:
            patches.append({
                'template_file': '',
                'line_pattern': r'def \w+\(.*\):',
                'replacement': '# Add None check: if value is None: raise ValueError("Value cannot be None")',
                'reason': 'Add None validation'
            })

        return patches

    def _generate_security_patches(self, pattern: Dict[str, Any], description: str) -> List[Dict[str, Any]]:
        """Generate patches for security issues"""
        patches = []

        # eval() usage
        if 'eval' in description:
            patches.append({
                'template_file': 'calculator.py',
                'line_pattern': r'return eval\(',
                'replacement': '''# Use ast.literal_eval() instead of eval() for safe evaluation
        try:
            return ast.literal_eval(expr)
        except (ValueError, SyntaxError):
            raise ValueError("Invalid expression")''',
                'reason': 'Replace eval() with ast.literal_eval() to prevent code injection'
            })

        # SQL injection
        if 'sql' in description and 'injection' in description:
            patches.append({
                'template_file': '',
                'line_pattern': r'execute\(["\'].*\+.*["\']\)',
                'replacement': 'execute(query, params)  # Use parameterized queries',
                'reason': 'Prevent SQL injection with parameterized queries'
            })

        return patches

    def _generate_quality_patches(self, pattern: Dict[str, Any], description: str) -> List[Dict[str, Any]]:
        """Generate patches for code quality issues"""
        patches = []

        # Missing type hints
        if 'type hint' in description or 'type annotation' in description:
            patches.append({
                'template_file': '',
                'line_pattern': r'def (\w+)\((.*)\):',
                'replacement': r'def \1(\2) -> ReturnType:  # Add appropriate type annotations',
                'reason': 'Add type hints for better code clarity and type checking'
            })

        # Missing docstrings
        if 'docstring' in description:
            patches.append({
                'template_file': '',
                'line_pattern': r'def (\w+)\((.*)\):$',
                'replacement': '''def \\1(\\2):
        """
        Brief description of what this function does.

        Args:
            param: Description

        Returns:
            Description of return value
        """''',
                'reason': 'Add docstring for better documentation'
            })

        # Unused variables
        if 'unused' in description and 'variable' in description:
            patches.append({
                'template_file': '',
                'line_pattern': r'(\s+)(\w+) = .*\n',
                'replacement': r'\1# Remove unused variable: \2\n',
                'reason': 'Remove unused variables to clean up code'
            })

        return patches

    def _generate_style_patches(self, pattern: Dict[str, Any], description: str) -> List[Dict[str, Any]]:
        """Generate patches for style issues"""
        patches = []

        # Naming conventions
        if 'naming' in description or 'convention' in description:
            patches.append({
                'template_file': '',
                'line_pattern': '',
                'replacement': '',
                'reason': 'Follow PEP 8 naming conventions (snake_case for functions/variables)'
            })

        return patches

    def _generate_performance_patches(self, pattern: Dict[str, Any], description: str) -> List[Dict[str, Any]]:
        """Generate patches for performance issues"""
        patches = []

        # Inefficient loops
        if 'loop' in description or 'iteration' in description:
            patches.append({
                'template_file': '',
                'line_pattern': '',
                'replacement': '# Consider using list comprehension or generator expression',
                'reason': 'Optimize loop performance'
            })

        return patches

    def _generate_generic_patch(self, pattern: Dict[str, Any], description: str) -> List[Dict[str, Any]]:
        """Generate generic patch for unrecognized patterns"""
        return [{
            'template_file': '',
            'line_pattern': '',
            'replacement': f'# TODO: Address issue - {pattern["description"]}',
            'reason': pattern['description']
        }]

    def get_learning_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the learning process.

        Returns:
            Dictionary with learning statistics
        """
        kb_stats = self.knowledge_base.get_stats()

        return {
            'total_findings': kb_stats['total_findings'],
            'total_patterns': kb_stats['total_patterns'],
            'total_patches': kb_stats['total_improvements'],
            'findings_by_severity': kb_stats['findings_by_severity'],
            'top_issues': kb_stats['top_issues'],
            'learning_rate': self._calculate_learning_rate(kb_stats)
        }

    def _calculate_learning_rate(self, stats: Dict[str, Any]) -> float:
        """
        Calculate how effectively the system is learning.

        Args:
            stats: Knowledge base statistics

        Returns:
            Learning rate (0-1)
        """
        findings = stats.get('total_findings', 0)
        patterns = stats.get('total_patterns', 0)
        patches = stats.get('total_improvements', 0)

        if findings == 0:
            return 0.0

        # Learning rate = (patterns + patches) / findings
        # Higher rate means more effective learning from data
        rate = (patterns + patches) / findings
        return min(rate, 1.0)  # Cap at 1.0
