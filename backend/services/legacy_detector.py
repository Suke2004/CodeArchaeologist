"""
Legacy code pattern detection module.
Identifies outdated patterns, deprecated APIs, and security vulnerabilities.
"""

from typing import Dict, List, Tuple
from enum import Enum
import re


class Severity(Enum):
    """Severity levels for detected issues."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Issue:
    """Represents a detected legacy code issue."""
    
    def __init__(
        self,
        severity: Severity,
        pattern: str,
        description: str,
        line_number: int = 0,
        suggestion: str = ""
    ):
        self.severity = severity
        self.pattern = pattern
        self.description = description
        self.line_number = line_number
        self.suggestion = suggestion
    
    def to_dict(self) -> Dict:
        return {
            "severity": self.severity.value,
            "pattern": self.pattern,
            "description": self.description,
            "line_number": self.line_number,
            "suggestion": self.suggestion
        }


class LegacyDetector:
    """Detects legacy patterns in code."""
    
    # Python 2 patterns
    PYTHON2_PATTERNS = [
        (r'print\s+"', Severity.HIGH, "Python 2 print statement", "Use print() function"),
        (r'print\s+\'', Severity.HIGH, "Python 2 print statement", "Use print() function"),
        (r'except\s+\w+\s*,\s*\w+:', Severity.HIGH, "Python 2 exception syntax", "Use 'except Exception as e:'"),
        (r'\.iteritems\(\)', Severity.HIGH, "Python 2 dict method", "Use .items()"),
        (r'\.iterkeys\(\)', Severity.HIGH, "Python 2 dict method", "Use .keys()"),
        (r'\.itervalues\(\)', Severity.HIGH, "Python 2 dict method", "Use .values()"),
        (r'\bxrange\(', Severity.HIGH, "Python 2 xrange", "Use range()"),
        (r'\bunicode\(', Severity.HIGH, "Python 2 unicode", "Use str()"),
        (r'"\s*%\s*\(', Severity.MEDIUM, "Old string formatting", "Use f-strings"),
        (r"'\s*%\s*\(", Severity.MEDIUM, "Old string formatting", "Use f-strings"),
        (r'\.format\(', Severity.LOW, "Old string formatting", "Consider f-strings"),
    ]
    
    # Security patterns
    SECURITY_PATTERNS = [
        (r'eval\(', Severity.CRITICAL, "Unsafe eval usage", "Avoid eval, use ast.literal_eval"),
        (r'exec\(', Severity.CRITICAL, "Unsafe exec usage", "Avoid exec"),
        (r'pickle\.loads?\(', Severity.HIGH, "Insecure deserialization", "Use json or safer alternatives"),
        (r'md5\(', Severity.HIGH, "Weak hash algorithm", "Use SHA-256 or better"),
        (r'sha1\(', Severity.HIGH, "Weak hash algorithm", "Use SHA-256 or better"),
    ]
    
    # Deprecated patterns
    DEPRECATED_PATTERNS = [
        (r'from __future__ import', Severity.MEDIUM, "Python 2 compatibility", "Remove if Python 3 only"),
        (r'file\(', Severity.HIGH, "Deprecated file() builtin", "Use open()"),
        (r'raw_input\(', Severity.HIGH, "Python 2 raw_input", "Use input()"),
    ]
    
    def detect_python_issues(self, code: str) -> List[Issue]:
        """
        Detect legacy patterns in Python code.
        
        Args:
            code: Python source code to analyze
        
        Returns:
            List of detected issues
        """
        issues: List[Issue] = []
        lines = code.split('\n')
        
        all_patterns = (
            self.PYTHON2_PATTERNS +
            self.SECURITY_PATTERNS +
            self.DEPRECATED_PATTERNS
        )
        
        for line_num, line in enumerate(lines, start=1):
            for pattern, severity, description, suggestion in all_patterns:
                if re.search(pattern, line):
                    issues.append(Issue(
                        severity=severity,
                        pattern=pattern,
                        description=description,
                        line_number=line_num,
                        suggestion=suggestion
                    ))
        
        return issues
    
    def generate_report(self, issues: List[Issue]) -> Dict:
        """
        Generate a summary report of detected issues.
        
        Args:
            issues: List of detected issues
        
        Returns:
            Dictionary with issue counts and details
        """
        severity_counts = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 0,
            Severity.MEDIUM: 0,
            Severity.LOW: 0
        }
        
        for issue in issues:
            severity_counts[issue.severity] += 1
        
        return {
            "total_issues": len(issues),
            "critical": severity_counts[Severity.CRITICAL],
            "high": severity_counts[Severity.HIGH],
            "medium": severity_counts[Severity.MEDIUM],
            "low": severity_counts[Severity.LOW],
            "issues": [issue.to_dict() for issue in issues]
        }
    
    def calculate_tech_debt(self, issues: List[Issue]) -> Dict:
        """
        Calculate technical debt metrics.
        
        Args:
            issues: List of detected issues
        
        Returns:
            Dictionary with tech debt metrics
        """
        # Estimate time to fix (in hours)
        time_estimates = {
            Severity.CRITICAL: 4,
            Severity.HIGH: 2,
            Severity.MEDIUM: 1,
            Severity.LOW: 0.5
        }
        
        total_hours = sum(
            time_estimates[issue.severity]
            for issue in issues
        )
        
        # Calculate maintainability score (0-100)
        max_score = 100
        penalty_per_issue = {
            Severity.CRITICAL: 10,
            Severity.HIGH: 5,
            Severity.MEDIUM: 2,
            Severity.LOW: 1
        }
        
        score = max_score - sum(
            penalty_per_issue[issue.severity]
            for issue in issues
        )
        score = max(0, min(100, score))
        
        # Determine grade
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        
        return {
            "estimated_hours": round(total_hours, 1),
            "estimated_days": round(total_hours / 8, 1),
            "maintainability_score": score,
            "grade": grade,
            "recommendation": self._get_recommendation(grade)
        }
    
    def _get_recommendation(self, grade: str) -> str:
        """Get recommendation based on grade."""
        recommendations = {
            "A": "Excellent! Code is modern and maintainable.",
            "B": "Good code quality. Minor improvements recommended.",
            "C": "Moderate technical debt. Consider refactoring.",
            "D": "Significant technical debt. Refactoring recommended.",
            "F": "Critical technical debt. Immediate modernization required."
        }
        return recommendations.get(grade, "Unknown grade")


# Example usage
if __name__ == "__main__":
    detector = LegacyDetector()
    
    sample_code = """
print "Hello, World!"

def process_data(data):
    for key, value in data.iteritems():
        print "Key: %s, Value: %s" % (key, value)

try:
    result = eval(user_input)
except Exception, e:
    print e
"""
    
    issues = detector.detect_python_issues(sample_code)
    report = detector.generate_report(issues)
    tech_debt = detector.calculate_tech_debt(issues)
    
    print("Detection Report:")
    print(f"Total Issues: {report['total_issues']}")
    print(f"Critical: {report['critical']}")
    print(f"High: {report['high']}")
    print(f"Medium: {report['medium']}")
    print(f"Low: {report['low']}")
    print(f"\nTechnical Debt:")
    print(f"Estimated Time: {tech_debt['estimated_days']} days")
    print(f"Maintainability: {tech_debt['maintainability_score']}/100 (Grade: {tech_debt['grade']})")
    print(f"Recommendation: {tech_debt['recommendation']}")
