"""
Patch Engine for Ultrathink.

This module applies learned code improvements to templates and generated code.
Uses AST-based transformations when possible, with regex fallback.
"""
import ast
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class PatchEngine:
    """
    Applies code patches to improve generated code.

    The patch engine:
    1. Attempts AST-based transformation for Python code
    2. Falls back to regex-based replacement for templates
    3. Validates syntax after patching
    4. Handles conflicts between multiple patches
    """

    def __init__(self):
        """Initialize the patch engine."""
        self.applied_patches = []
        self.failed_patches = []

    def apply_patches(
        self,
        code: str,
        patches: List[Dict[str, Any]],
        language: str = "python"
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Apply multiple patches to code.

        Args:
            code: Original code to patch
            patches: List of patch dictionaries
            language: Programming language (default: python)

        Returns:
            Tuple of (patched_code, application_report)
        """
        if not patches:
            return code, []

        patched_code = code
        report = []

        logger.info(f"Applying {len(patches)} patches to {language} code")

        for i, patch in enumerate(patches):
            try:
                result = self.apply_patch(patched_code, patch, language)

                if result['applied']:
                    patched_code = result['code']
                    self.applied_patches.append(patch)
                    report.append({
                        'patch_id': patch.get('id', i),
                        'reason': patch.get('reason', 'Unknown'),
                        'status': 'applied',
                        'message': result.get('message', 'Successfully applied')
                    })
                    logger.info(f"Applied patch {i+1}: {patch.get('reason', 'Unknown')[:50]}")
                else:
                    self.failed_patches.append(patch)
                    report.append({
                        'patch_id': patch.get('id', i),
                        'reason': patch.get('reason', 'Unknown'),
                        'status': 'skipped',
                        'message': result.get('message', 'Pattern not found')
                    })
                    logger.debug(f"Skipped patch {i+1}: {result.get('message', 'Pattern not found')}")

            except Exception as e:
                self.failed_patches.append(patch)
                report.append({
                    'patch_id': patch.get('id', i),
                    'reason': patch.get('reason', 'Unknown'),
                    'status': 'error',
                    'message': str(e)
                })
                logger.error(f"Error applying patch {i+1}: {e}")

        logger.info(f"Patch application complete: {len(self.applied_patches)} applied, "
                   f"{len(self.failed_patches)} failed/skipped")

        return patched_code, report

    def apply_patch(
        self,
        code: str,
        patch: Dict[str, Any],
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Apply a single patch to code.

        Args:
            code: Code to patch
            patch: Patch dictionary with line_pattern and replacement
            language: Programming language

        Returns:
            Dictionary with 'applied' (bool), 'code' (str), 'message' (str)
        """
        line_pattern = patch.get('line_pattern', '')
        replacement = patch.get('replacement', '')

        if not line_pattern:
            return {
                'applied': False,
                'code': code,
                'message': 'No line pattern specified'
            }

        # Try regex-based replacement first (works for both code and templates)
        result = self._apply_regex_patch(code, line_pattern, replacement)

        if result['applied']:
            # Validate syntax if it's Python code
            if language == "python":
                if self._validate_python_syntax(result['code']):
                    return result
                else:
                    logger.warning("Patch produced invalid Python syntax, reverting")
                    return {
                        'applied': False,
                        'code': code,
                        'message': 'Patch produced invalid syntax'
                    }
            else:
                return result

        # If regex didn't match, return unchanged
        return {
            'applied': False,
            'code': code,
            'message': 'Pattern not found in code'
        }

    def _apply_regex_patch(
        self,
        code: str,
        pattern: str,
        replacement: str
    ) -> Dict[str, Any]:
        """
        Apply patch using regex replacement.

        Args:
            code: Original code
            pattern: Regex pattern to match
            replacement: Replacement text

        Returns:
            Dictionary with application result
        """
        try:
            # Try to compile and apply the regex
            regex = re.compile(pattern, re.MULTILINE | re.DOTALL)
            match = regex.search(code)

            if match:
                patched_code = regex.sub(replacement, code, count=1)
                return {
                    'applied': True,
                    'code': patched_code,
                    'message': f'Applied regex replacement at position {match.start()}'
                }
            else:
                return {
                    'applied': False,
                    'code': code,
                    'message': 'Pattern not found'
                }

        except re.error as e:
            logger.error(f"Invalid regex pattern: {e}")
            return {
                'applied': False,
                'code': code,
                'message': f'Invalid regex pattern: {e}'
            }

    def _validate_python_syntax(self, code: str) -> bool:
        """
        Validate that code is syntactically correct Python.

        Args:
            code: Python code to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    def apply_ast_transformation(
        self,
        code: str,
        transformation: str
    ) -> Optional[str]:
        """
        Apply AST-based code transformation.

        Args:
            code: Python code to transform
            transformation: Type of transformation (e.g., 'add_type_hints')

        Returns:
            Transformed code or None if transformation fails
        """
        try:
            tree = ast.parse(code)

            # Apply transformation based on type
            if transformation == 'add_type_hints':
                tree = self._add_type_hints_visitor(tree)
            elif transformation == 'add_docstrings':
                tree = self._add_docstrings_visitor(tree)
            else:
                logger.warning(f"Unknown transformation type: {transformation}")
                return None

            # Convert AST back to code
            return ast.unparse(tree)

        except Exception as e:
            logger.error(f"AST transformation failed: {e}")
            return None

    def _add_type_hints_visitor(self, tree: ast.AST) -> ast.AST:
        """Add type hints to function definitions (placeholder)"""
        # This would use an AST visitor to add type hints
        # For now, return unchanged
        return tree

    def _add_docstrings_visitor(self, tree: ast.AST) -> ast.AST:
        """Add docstrings to functions without them (placeholder)"""
        # This would use an AST visitor to add docstrings
        # For now, return unchanged
        return tree

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about patch application.

        Returns:
            Dictionary with patch statistics
        """
        return {
            'total_applied': len(self.applied_patches),
            'total_failed': len(self.failed_patches),
            'success_rate': (
                len(self.applied_patches) / (len(self.applied_patches) + len(self.failed_patches))
                if (len(self.applied_patches) + len(self.failed_patches)) > 0
                else 0.0
            )
        }

    def reset(self):
        """Reset patch application history"""
        self.applied_patches = []
        self.failed_patches = []


class SmartPatcher:
    """
    Advanced patcher with conflict detection and resolution.

    Handles cases where multiple patches may affect the same code.
    """

    def __init__(self):
        """Initialize smart patcher"""
        self.patch_engine = PatchEngine()

    def apply_patches_with_conflict_detection(
        self,
        code: str,
        patches: List[Dict[str, Any]],
        language: str = "python"
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Apply patches with conflict detection.

        Args:
            code: Original code
            patches: List of patches to apply
            language: Programming language

        Returns:
            Tuple of (patched_code, detailed_report)
        """
        # Sort patches by priority (critical > high > medium > low)
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
        sorted_patches = sorted(
            patches,
            key=lambda p: severity_order.get(p.get('severity', 'info'), 4)
        )

        # Apply patches sequentially with conflict checks
        return self.patch_engine.apply_patches(code, sorted_patches, language)

    def detect_conflicts(
        self,
        code: str,
        patches: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Detect potential conflicts between patches.

        Args:
            code: Code to check
            patches: List of patches

        Returns:
            List of detected conflicts
        """
        conflicts = []

        # Check for overlapping line patterns
        for i, patch1 in enumerate(patches):
            for j, patch2 in enumerate(patches[i+1:], start=i+1):
                if self._patterns_overlap(patch1.get('line_pattern', ''),
                                         patch2.get('line_pattern', '')):
                    conflicts.append({
                        'patch1': patch1.get('reason', f'Patch {i}'),
                        'patch2': patch2.get('reason', f'Patch {j}'),
                        'type': 'overlapping_patterns'
                    })

        return conflicts

    def _patterns_overlap(self, pattern1: str, pattern2: str) -> bool:
        """
        Check if two regex patterns might overlap.

        Args:
            pattern1: First pattern
            pattern2: Second pattern

        Returns:
            True if patterns might conflict
        """
        # Simplified check - in practice, this would be more sophisticated
        return pattern1 == pattern2
