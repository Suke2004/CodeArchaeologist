"""
Comprehensive test suite for legacy pattern detection.
Tests all detection rules, severity classification, and tech debt calculation.
"""

import pytest
from services.legacy_detector import LegacyDetector, Severity, Issue


class TestLegacyDetector:
    """Test suite for LegacyDetector class."""
    
    @pytest.fixture
    def detector(self):
        """Create a LegacyDetector instance for testing."""
        return LegacyDetector()
    
    # Python 2 Pattern Tests
    
    def test_detect_python2_print_statement_double_quotes(self, detector):
        """Test detection of Python 2 print statements with double quotes."""
        code = 'print "Hello, World!"'
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any(issue.severity == Severity.HIGH for issue in issues)
        assert any("print statement" in issue.description.lower() for issue in issues)
    
    def test_detect_python2_print_statement_single_quotes(self, detector):
        """Test detection of Python 2 print statements with single quotes."""
        code = "print 'Hello, World!'"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any(issue.severity == Severity.HIGH for issue in issues)
    
    def test_detect_python2_exception_syntax(self, detector):
        """Test detection of Python 2 exception handling syntax."""
        code = """
try:
    risky_operation()
except Exception, e:
    print e
"""
        issues = detector.detect_python_issues(code)
        
        assert len(issues) >= 1  # except syntax (print without quotes not detected)
        assert any("exception syntax" in issue.description.lower() for issue in issues)
    
    def test_detect_iteritems(self, detector):
        """Test detection of dict.iteritems() method."""
        code = "for k, v in data.iteritems():"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("iteritems" in issue.pattern for issue in issues)
        assert any(issue.severity == Severity.HIGH for issue in issues)
    
    def test_detect_iterkeys(self, detector):
        """Test detection of dict.iterkeys() method."""
        code = "for k in data.iterkeys():"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("iterkeys" in issue.pattern for issue in issues)
    
    def test_detect_itervalues(self, detector):
        """Test detection of dict.itervalues() method."""
        code = "for v in data.itervalues():"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("itervalues" in issue.pattern for issue in issues)
    
    def test_detect_xrange(self, detector):
        """Test detection of xrange() function."""
        code = "for i in xrange(10):"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("xrange" in issue.description.lower() for issue in issues)
        assert any("range()" in issue.suggestion for issue in issues)
    
    def test_detect_unicode_builtin(self, detector):
        """Test detection of unicode() builtin."""
        code = "text = unicode(data)"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("unicode" in issue.description.lower() for issue in issues)
    
    def test_detect_old_string_formatting_percent(self, detector):
        """Test detection of % string formatting."""
        code = 'result = "Hello, %s" % (name,)'
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("string formatting" in issue.description.lower() for issue in issues)
    
    def test_detect_format_method(self, detector):
        """Test detection of .format() string formatting."""
        code = '"Hello, {}".format(name)'
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any(issue.severity == Severity.LOW for issue in issues)
    
    # Security Pattern Tests
    
    def test_detect_eval_usage(self, detector):
        """Test detection of unsafe eval() usage."""
        code = "result = eval(user_input)"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any(issue.severity == Severity.CRITICAL for issue in issues)
        assert any("eval" in issue.description.lower() for issue in issues)
    
    def test_detect_exec_usage(self, detector):
        """Test detection of unsafe exec() usage."""
        code = "exec(user_code)"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any(issue.severity == Severity.CRITICAL for issue in issues)
    
    def test_detect_pickle_loads(self, detector):
        """Test detection of insecure pickle.loads()."""
        code = "import pickle\ndata = pickle.loads(untrusted_data)"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any(issue.severity == Severity.HIGH for issue in issues)
        assert any("deserialization" in issue.description.lower() for issue in issues)
    
    def test_detect_md5_hash(self, detector):
        """Test detection of weak MD5 hash algorithm."""
        code = "import hashlib\nhash = hashlib.md5(data)"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("hash algorithm" in issue.description.lower() for issue in issues)
    
    def test_detect_sha1_hash(self, detector):
        """Test detection of weak SHA1 hash algorithm."""
        code = "import hashlib\nhash = hashlib.sha1(data)"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("hash algorithm" in issue.description.lower() for issue in issues)
    
    # Deprecated Pattern Tests
    
    def test_detect_future_import(self, detector):
        """Test detection of __future__ imports."""
        code = "from __future__ import print_function"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("compatibility" in issue.description.lower() for issue in issues)
    
    def test_detect_file_builtin(self, detector):
        """Test detection of deprecated file() builtin."""
        code = "f = file('data.txt')"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("file()" in issue.description for issue in issues)
    
    def test_detect_raw_input(self, detector):
        """Test detection of Python 2 raw_input()."""
        code = "name = raw_input('Enter name: ')"
        issues = detector.detect_python_issues(code)
        
        assert len(issues) > 0
        assert any("raw_input" in issue.description.lower() for issue in issues)
    
    # Line Number Tests
    
    def test_line_numbers_are_correct(self, detector):
        """Test that line numbers are correctly reported."""
        code = """line 1
print "line 2"
line 3
for k, v in data.iteritems():
    pass
"""
        issues = detector.detect_python_issues(code)
        
        print_issue = next((i for i in issues if "print" in i.description.lower()), None)
        iteritems_issue = next((i for i in issues if "iteritems" in i.pattern), None)
        
        assert print_issue is not None
        assert print_issue.line_number == 2
        assert iteritems_issue is not None
        assert iteritems_issue.line_number == 4
    
    # Report Generation Tests
    
    def test_generate_report_counts(self, detector):
        """Test that report correctly counts issues by severity."""
        code = """
print "test"  # HIGH
result = eval(x)  # CRITICAL
text = "Hello %s" % (name,)  # MEDIUM
"""
        issues = detector.detect_python_issues(code)
        report = detector.generate_report(issues)
        
        assert report['total_issues'] == len(issues)
        assert report['critical'] >= 1  # eval
        assert report['high'] >= 1  # print
        assert isinstance(report['issues'], list)
    
    def test_generate_report_structure(self, detector):
        """Test that report has correct structure."""
        code = 'print "test"'
        issues = detector.detect_python_issues(code)
        report = detector.generate_report(issues)
        
        assert 'total_issues' in report
        assert 'critical' in report
        assert 'high' in report
        assert 'medium' in report
        assert 'low' in report
        assert 'issues' in report
        
        if report['issues']:
            issue_dict = report['issues'][0]
            assert 'severity' in issue_dict
            assert 'pattern' in issue_dict
            assert 'description' in issue_dict
            assert 'line_number' in issue_dict
            assert 'suggestion' in issue_dict
    
    # Technical Debt Tests
    
    def test_calculate_tech_debt_hours(self, detector):
        """Test that tech debt hours are calculated correctly."""
        code = """
print "test"  # HIGH = 2 hours
result = eval(x)  # CRITICAL = 4 hours
text = "Hello %s" % name  # MEDIUM = 1 hour
"""
        issues = detector.detect_python_issues(code)
        tech_debt = detector.calculate_tech_debt(issues)
        
        assert tech_debt['estimated_hours'] > 0
        assert tech_debt['estimated_days'] > 0
        assert tech_debt['estimated_days'] == round(tech_debt['estimated_hours'] / 8, 1)
    
    def test_calculate_tech_debt_score(self, detector):
        """Test that maintainability score is calculated correctly."""
        code = 'print "test"'
        issues = detector.detect_python_issues(code)
        tech_debt = detector.calculate_tech_debt(issues)
        
        assert 0 <= tech_debt['maintainability_score'] <= 100
        assert tech_debt['grade'] in ['A', 'B', 'C', 'D', 'F']
    
    def test_calculate_tech_debt_grade_a(self, detector):
        """Test that clean code gets grade A."""
        code = """
def modern_function(x: int) -> int:
    return x * 2
"""
        issues = detector.detect_python_issues(code)
        tech_debt = detector.calculate_tech_debt(issues)
        
        assert tech_debt['grade'] == 'A'
        assert tech_debt['maintainability_score'] >= 90
    
    def test_calculate_tech_debt_grade_f(self, detector):
        """Test that heavily legacy code gets grade F."""
        code = """
print "test1"
print "test2"
print "test3"
eval(x)
exec(y)
for k, v in d.iteritems():
    print "item"
result = eval(user_input)
"""
        issues = detector.detect_python_issues(code)
        tech_debt = detector.calculate_tech_debt(issues)
        
        assert tech_debt['grade'] == 'F'
        assert tech_debt['maintainability_score'] < 60
    
    def test_tech_debt_recommendation(self, detector):
        """Test that recommendations are provided."""
        code = 'print "test"'
        issues = detector.detect_python_issues(code)
        tech_debt = detector.calculate_tech_debt(issues)
        
        assert 'recommendation' in tech_debt
        assert len(tech_debt['recommendation']) > 0
    
    # Edge Cases
    
    def test_empty_code(self, detector):
        """Test handling of empty code."""
        code = ""
        issues = detector.detect_python_issues(code)
        
        assert len(issues) == 0
    
    def test_modern_code_no_issues(self, detector):
        """Test that modern code produces no issues."""
        code = """
from typing import Dict, List

def process_data(data: Dict[str, int]) -> List[int]:
    \"\"\"Process data with modern Python.\"\"\"
    return [value * 2 for key, value in data.items()]

if __name__ == "__main__":
    print("Hello, World!")
"""
        issues = detector.detect_python_issues(code)
        
        assert len(issues) == 0
    
    def test_multiple_issues_same_line(self, detector):
        """Test detection of multiple issues on the same line."""
        code = 'print "test: %s" % (value,)'
        issues = detector.detect_python_issues(code)
        
        # Should detect print statement and possibly % formatting
        assert len(issues) >= 1
    
    def test_issue_to_dict(self, detector):
        """Test Issue.to_dict() method."""
        issue = Issue(
            severity=Severity.HIGH,
            pattern=r'print\s+"',
            description="Python 2 print statement",
            line_number=5,
            suggestion="Use print() function"
        )
        
        issue_dict = issue.to_dict()
        
        assert issue_dict['severity'] == 'HIGH'
        assert issue_dict['pattern'] == r'print\s+"'
        assert issue_dict['description'] == "Python 2 print statement"
        assert issue_dict['line_number'] == 5
        assert issue_dict['suggestion'] == "Use print() function"


class TestSeverityEnum:
    """Test suite for Severity enum."""
    
    def test_severity_values(self):
        """Test that severity enum has correct values."""
        assert Severity.CRITICAL.value == "CRITICAL"
        assert Severity.HIGH.value == "HIGH"
        assert Severity.MEDIUM.value == "MEDIUM"
        assert Severity.LOW.value == "LOW"


class TestIntegration:
    """Integration tests for complete workflows."""
    
    @pytest.fixture
    def detector(self):
        return LegacyDetector()
    
    def test_full_analysis_workflow(self, detector):
        """Test complete analysis workflow from code to report."""
        legacy_code = """
print "Starting analysis..."

def fetch_users(callback):
    users = []
    for i in xrange(10):
        user = {'id': i, 'name': 'User %s' % (i,)}
        users.append(user)
    callback(users)

try:
    result = eval(user_input)
except Exception, e:
    print e
"""
        
        # Detect issues
        issues = detector.detect_python_issues(legacy_code)
        assert len(issues) > 0
        
        # Generate report
        report = detector.generate_report(issues)
        assert report['total_issues'] > 0
        assert report['critical'] > 0  # eval usage
        assert report['high'] > 0  # print statements, exception syntax
        
        # Calculate tech debt
        tech_debt = detector.calculate_tech_debt(issues)
        assert tech_debt['estimated_hours'] > 0
        assert tech_debt['grade'] in ['C', 'D', 'F']  # Should be poor to moderate grade
        assert 'recommendation' in tech_debt
    
    def test_comparison_legacy_vs_modern(self, detector):
        """Test that modern code scores better than legacy code."""
        legacy_code = """
print "Hello"
for k, v in data.iteritems():
    print "Key: %s" % k
"""
        
        modern_code = """
from typing import Dict

def process_data(data: Dict[str, str]) -> None:
    for key, value in data.items():
        print(f"Key: {key}")

if __name__ == "__main__":
    print("Hello")
"""
        
        legacy_issues = detector.detect_python_issues(legacy_code)
        modern_issues = detector.detect_python_issues(modern_code)
        
        legacy_debt = detector.calculate_tech_debt(legacy_issues)
        modern_debt = detector.calculate_tech_debt(modern_issues)
        
        assert len(legacy_issues) > len(modern_issues)
        assert legacy_debt['maintainability_score'] < modern_debt['maintainability_score']
        assert legacy_debt['estimated_hours'] > modern_debt['estimated_hours']


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
