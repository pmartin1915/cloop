"""
Knowledge Base for storing and retrieving learned information.

This module manages the persistent storage of insights, patterns, and
improvements discovered by the system.
"""
import hashlib
import json
import logging
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Persistent storage for learned patterns and improvements"""

    def __init__(self, db_path: str = "ultrathink.db"):
        """
        Initialize the knowledge base.

        Args:
            db_path: Path to database file
        """
        self.db_path = db_path
        self.patterns = []
        self.improvements = []

        # Initialize database
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Initialize SQLite database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create findings table for storing analysis results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                line_number INTEGER,
                severity TEXT,
                category TEXT,
                description TEXT NOT NULL,
                suggestion TEXT,
                code_snippet TEXT,
                timestamp TEXT NOT NULL,
                UNIQUE(file_path, line_number, description)
            )
        ''')

        # Create patterns table for learned patterns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,
                description TEXT NOT NULL,
                context TEXT,
                frequency INTEGER DEFAULT 1,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL
            )
        ''')

        # Create improvements/patches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS improvements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT,
                template_file TEXT,
                line_pattern TEXT,
                replacement TEXT,
                reason TEXT,
                applied_count INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (pattern_id) REFERENCES patterns(id)
            )
        ''')

        # Create indexes for faster queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_findings_severity ON findings(severity)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_findings_category ON findings(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_findings_file ON findings(file_path)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patterns_type ON patterns(pattern_type)')

        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")

    def store_analysis_findings(
        self,
        file_path: str,
        findings: List[Dict[str, Any]],
        parse_info: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Store findings from code analysis.

        Args:
            file_path: Path to analyzed file
            findings: List of finding dictionaries from analysis
            parse_info: Optional parse metadata
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        stored_count = 0

        for finding in findings:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO findings
                    (file_path, line_number, severity, category, description, suggestion, code_snippet, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    file_path,
                    finding.get('line_number'),
                    finding.get('severity', 'info'),
                    finding.get('category', 'unknown'),
                    finding.get('description', finding.get('raw_response', 'No description')),
                    finding.get('suggestion', ''),
                    finding.get('code_snippet', ''),
                    timestamp
                ))
                stored_count += 1
            except sqlite3.IntegrityError:
                # Duplicate finding, skip
                logger.debug(f"Duplicate finding skipped: {finding.get('description', '')[:50]}")
                continue

        conn.commit()
        conn.close()
        logger.info(f"Stored {stored_count} findings from {file_path}")

    def get_recurring_issues(self, threshold: int = 2) -> List[Dict[str, Any]]:
        """
        Find recurring issues across multiple files.

        Args:
            threshold: Minimum occurrences to consider as recurring

        Returns:
            List of recurring issue patterns
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Group findings by description and category to find patterns
        cursor.execute('''
            SELECT
                description,
                category,
                severity,
                COUNT(*) as frequency,
                MIN(timestamp) as first_seen,
                MAX(timestamp) as last_seen,
                GROUP_CONCAT(file_path) as affected_files
            FROM findings
            GROUP BY description, category
            HAVING COUNT(*) >= ?
            ORDER BY frequency DESC
        ''', (threshold,))

        recurring = []
        for row in cursor.fetchall():
            recurring.append({
                'description': row[0],
                'category': row[1],
                'severity': row[2],
                'frequency': row[3],
                'first_seen': row[4],
                'last_seen': row[5],
                'affected_files': row[6].split(',') if row[6] else []
            })

        conn.close()
        logger.info(f"Found {len(recurring)} recurring issues (threshold: {threshold})")
        return recurring

    def store_pattern(self, pattern: Dict[str, Any]):
        """Store a learned pattern"""
        pattern_id = hashlib.md5(
            json.dumps({
                'type': pattern.get('pattern_type', 'unknown'),
                'desc': pattern.get('description', '')
            }).encode()
        ).hexdigest()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()

        try:
            # Try to insert new pattern
            cursor.execute('''
                INSERT INTO patterns (id, pattern_type, description, context, frequency, first_seen, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern_id,
                pattern.get('pattern_type', 'unknown'),
                pattern.get('description', ''),
                json.dumps(pattern.get('context', {})),
                1,
                timestamp,
                timestamp
            ))
        except sqlite3.IntegrityError:
            # Pattern exists, update frequency and last_seen
            cursor.execute('''
                UPDATE patterns
                SET frequency = frequency + 1, last_seen = ?
                WHERE id = ?
            ''', (timestamp, pattern_id))

        conn.commit()
        conn.close()

        # Also keep in memory for backward compatibility
        self.patterns.append({
            **pattern,
            'timestamp': timestamp,
            'id': pattern_id
        })

    def find_similar_patterns(self, context: Dict[str, Any], threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Find similar patterns in knowledge base"""
        # Simplified similarity check
        similar = []
        for pattern in self.patterns:
            similarity = self._calculate_similarity(pattern, context)
            if similarity >= threshold:
                similar.append(pattern)
        return similar

    def _calculate_similarity(self, pattern: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calculate similarity between pattern and context"""
        # Simplified - would use proper similarity metrics
        return 0.5

    def save(self) -> None:
        """
        Save knowledge base to persistent storage.

        Note: With SQLite, data is saved immediately on each operation.
        This method is kept for API compatibility and can be used for
        explicit sync if needed.
        """
        # With SQLite, data is already persisted
        # Could add backup functionality here
        logger.info(f"Knowledge base persisted at {self.db_path}")

    def load(self) -> None:
        """Load knowledge base from persistent storage into memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Load patterns into memory
        cursor.execute('SELECT id, pattern_type, description, context, frequency, first_seen, last_seen FROM patterns')
        self.patterns = []
        for row in cursor.fetchall():
            self.patterns.append({
                'id': row[0],
                'pattern_type': row[1],
                'description': row[2],
                'context': json.loads(row[3]) if row[3] else {},
                'frequency': row[4],
                'first_seen': row[5],
                'last_seen': row[6]
            })

        # Load improvements into memory
        cursor.execute('SELECT id, pattern_id, template_file, line_pattern, replacement, reason, applied_count, created_at FROM improvements')
        self.improvements = []
        for row in cursor.fetchall():
            self.improvements.append({
                'id': row[0],
                'pattern_id': row[1],
                'template_file': row[2],
                'line_pattern': row[3],
                'replacement': row[4],
                'reason': row[5],
                'applied_count': row[6],
                'created_at': row[7]
            })

        conn.close()
        logger.info(f"Loaded {len(self.patterns)} patterns and {len(self.improvements)} improvements from {self.db_path}")

    def store_improvement(self, improvement: Dict[str, Any]) -> None:
        """
        Store a learned improvement/patch.

        Args:
            improvement: Dictionary with template_file, line_pattern, replacement, reason
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO improvements
            (pattern_id, template_file, line_pattern, replacement, reason, applied_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            improvement.get('pattern_id'),
            improvement.get('template_file', ''),
            improvement.get('line_pattern', ''),
            improvement.get('replacement', ''),
            improvement.get('reason', ''),
            0,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

        # Also add to memory list
        self.improvements.append(improvement)
        logger.info(f"Stored improvement for {improvement.get('template_file', 'unknown')}")

    def get_improvements_for_template(self, template_name: str) -> List[Dict[str, Any]]:
        """
        Get all applicable improvements for a specific template.

        Args:
            template_name: Name of template file

        Returns:
            List of applicable improvements
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, pattern_id, line_pattern, replacement, reason, applied_count
            FROM improvements
            WHERE template_file = ? OR template_file = ''
            ORDER BY applied_count ASC
        ''', (template_name,))

        improvements = []
        for row in cursor.fetchall():
            improvements.append({
                'id': row[0],
                'pattern_id': row[1],
                'line_pattern': row[2],
                'replacement': row[3],
                'reason': row[4],
                'applied_count': row[5]
            })

        conn.close()
        return improvements

    def increment_improvement_usage(self, improvement_id: int) -> None:
        """
        Increment the applied count for an improvement.

        Args:
            improvement_id: ID of the improvement
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE improvements
            SET applied_count = applied_count + 1
            WHERE id = ?
        ''', (improvement_id,))

        conn.commit()
        conn.close()

    def get_all_findings(self) -> List[Dict[str, Any]]:
        """Get all findings from the knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT file_path, line_number, severity, category, description, suggestion FROM findings ORDER BY timestamp DESC')
        findings = []
        for row in cursor.fetchall():
            findings.append({
                'file_path': row[0],
                'line_number': row[1],
                'severity': row[2],
                'category': row[3],
                'description': row[4],
                'suggestion': row[5]
            })
        
        conn.close()
        return findings
    
    def get_all_patterns(self) -> List[Dict[str, Any]]:
        """Get all patterns from the knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT pattern_type, description, frequency FROM patterns ORDER BY frequency DESC')
        patterns = []
        for row in cursor.fetchall():
            patterns.append({
                'pattern_type': row[0],
                'description': row[1],
                'frequency': row[2],
                'severity': 'medium'  # Default since not stored
            })
        
        conn.close()
        return patterns
    
    def get_all_improvements(self) -> List[Dict[str, Any]]:
        """Get all improvements from the knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT template_file, line_pattern, replacement, reason FROM improvements')
        improvements = []
        for row in cursor.fetchall():
            improvements.append({
                'template_file': row[0],
                'line_pattern': row[1],
                'replacement': row[2],
                'reason': row[3]
            })
        
        conn.close()
        return improvements

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Count findings
        cursor.execute('SELECT COUNT(*) FROM findings')
        stats['total_findings'] = cursor.fetchone()[0]

        # Count by severity
        cursor.execute('SELECT severity, COUNT(*) FROM findings GROUP BY severity')
        severity_dict = dict(cursor.fetchall())
        stats['findings_by_severity'] = severity_dict
        stats['severity_breakdown'] = severity_dict
        stats['learning_rate'] = (stats.get('total_improvements', 0) / max(stats.get('total_findings', 1), 1))

        # Count patterns
        cursor.execute('SELECT COUNT(*) FROM patterns')
        stats['total_patterns'] = cursor.fetchone()[0]

        # Count improvements
        cursor.execute('SELECT COUNT(*) FROM improvements')
        stats['total_improvements'] = cursor.fetchone()[0]

        # Most common issues
        cursor.execute('''
            SELECT description, COUNT(*) as count
            FROM findings
            GROUP BY description
            ORDER BY count DESC
            LIMIT 5
        ''')
        stats['top_issues'] = [{'description': row[0], 'count': row[1]} for row in cursor.fetchall()]

        conn.close()
        return stats
