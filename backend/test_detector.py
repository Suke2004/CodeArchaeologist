#!/usr/bin/env python3
"""
Interactive test script for legacy detector.
Run this to quickly test the detector without pytest.
"""

from services.legacy_detector import LegacyDetector
import json


def print_separator():
    """Print a visual separator."""
    print("\n" + "="*70 + "\n")


def test_basic_detection():
    """Test basic legacy pattern detection."""
    print("🔍 Testing Basic Legacy Pattern Detection")
    print_separator()
    
    detector = LegacyDetector()
    
    code = '''print "Hello, World!"
def test():
    for k, v in data.iteritems():
        print "Key: %s" % k
'''
    
    issues = detector.detect_python_issues(code)
    report = detector.generate_report(issues)
    tech_debt = detector.calculate_tech_debt(issues)
    
    print(f"📊 Detection Results:")
    print(f"  Total Issues: {report['total_issues']}")
    print(f"  Critical: {report['critical']}")
    print(f"  High: {report['high']}")
    print(f"  Medium: {report['medium']}")
    print(f"  Low: {report['low']}")
    
    print(f"\n💰 Technical Debt:")
    print(f"  Estimated Time: {tech_debt['estimated_days']} days ({tech_debt['estimated_hours']} hours)")
    print(f"  Maintainability: {tech_debt['maintainability_score']}/100 (Grade: {tech_debt['grade']})")
    print(f"  Recommendation: {tech_debt['recommendation']}")
    
    if report['issues']:
        print(f"\n🐛 First Issue Details:")
        first_issue = report['issues'][0]
        print(f"  Severity: {first_issue['severity']}")
        print(f"  Line: {first_issue['line_number']}")
        print(f"  Description: {first_issue['description']}")
        print(f"  Suggestion: {first_issue['suggestion']}")


def test_security_detection():
    """Test security vulnerability detection."""
    print("🔒 Testing Security Vulnerability Detection")
    print_separator()
    
    detector = LegacyDetector()
    
    code = '''
import pickle
import hashlib

def process_user_input(user_data):
    # Unsafe eval
    result = eval(user_data)
    
    # Insecure deserialization
    obj = pickle.loads(user_data)
    
    # Weak hash
    hash_val = hashlib.md5(user_data.encode()).hexdigest()
    
    return result
'''
    
    issues = detector.detect_python_issues(code)
    report = detector.generate_report(issues)
    
    print(f"🚨 Security Issues Found: {report['critical'] + report['high']}")
    
    for issue in report['issues']:
        if issue['severity'] in ['CRITICAL', 'HIGH']:
            print(f"\n  [{issue['severity']}] Line {issue['line_number']}")
            print(f"    Problem: {issue['description']}")
            print(f"    Fix: {issue['suggestion']}")


def test_comprehensive_legacy_code():
    """Test with comprehensive legacy code sample."""
    print("📦 Testing Comprehensive Legacy Code")
    print_separator()
    
    detector = LegacyDetector()
    
    legacy_code = '''
from __future__ import print_function
import pickle

print "Starting legacy application..."

def fetch_users(callback):
    """Fetch users using old patterns."""
    users = []
    for i in xrange(10):
        user = {'id': i, 'name': 'User %s' % i}
        users.append(user)
    callback(users)

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, id, name):
        self.users[id] = name
        print "Added user:", name
    
    def process_data(self, data):
        # Unsafe eval
        result = eval(data)
        
        # Insecure pickle
        serialized = pickle.dumps(result)
        
        return serialized

try:
    manager = UserManager()
    for key, value in manager.users.iteritems():
        print "User: %s" % value
except Exception, e:
    print e
'''
    
    issues = detector.detect_python_issues(legacy_code)
    report = detector.generate_report(issues)
    tech_debt = detector.calculate_tech_debt(issues)
    
    print(f"📈 Comprehensive Analysis:")
    print(f"  Total Issues: {report['total_issues']}")
    print(f"  By Severity:")
    print(f"    🔴 Critical: {report['critical']}")
    print(f"    🟠 High: {report['high']}")
    print(f"    🟡 Medium: {report['medium']}")
    print(f"    🟢 Low: {report['low']}")
    
    print(f"\n  Technical Debt:")
    print(f"    Time to Fix: {tech_debt['estimated_days']} days")
    print(f"    Code Grade: {tech_debt['grade']}")
    print(f"    Score: {tech_debt['maintainability_score']}/100")
    
    print(f"\n  Issue Breakdown:")
    issue_types = {}
    for issue in report['issues']:
        desc = issue['description']
        issue_types[desc] = issue_types.get(desc, 0) + 1
    
    for desc, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
        print(f"    • {desc}: {count}x")


def test_modern_code():
    """Test that modern code produces no issues."""
    print("✨ Testing Modern Code (Should be Clean)")
    print_separator()
    
    detector = LegacyDetector()
    
    modern_code = '''
from typing import Dict, List, Callable

def fetch_users() -> List[Dict[str, str]]:
    """Fetch users with modern patterns."""
    return [
        {'id': str(i), 'name': f'User {i}'}
        for i in range(10)
    ]

class UserManager:
    """Modern user manager with type hints."""
    
    def __init__(self) -> None:
        self.users: Dict[int, str] = {}
    
    def add_user(self, user_id: int, name: str) -> None:
        """Add a user to the manager."""
        self.users[user_id] = name
        print(f"Added user: {name}")
    
    def get_all_users(self) -> Dict[int, str]:
        """Get all users."""
        return self.users.copy()

if __name__ == "__main__":
    print("Starting modern application...")
    manager = UserManager()
    users = fetch_users()
    
    for user in users:
        manager.add_user(int(user['id']), user['name'])
'''
    
    issues = detector.detect_python_issues(modern_code)
    report = detector.generate_report(issues)
    tech_debt = detector.calculate_tech_debt(issues)
    
    if report['total_issues'] == 0:
        print("✅ Perfect! No legacy patterns detected.")
        print(f"   Maintainability Score: {tech_debt['maintainability_score']}/100")
        print(f"   Grade: {tech_debt['grade']}")
    else:
        print(f"⚠️  Found {report['total_issues']} issues (unexpected)")
        for issue in report['issues']:
            print(f"   Line {issue['line_number']}: {issue['description']}")


def main():
    """Run all tests."""
    print("\n" + "🏛️  CodeArchaeologist - Legacy Detector Test Suite".center(70))
    print("="*70)
    
    try:
        test_basic_detection()
        print_separator()
        
        test_security_detection()
        print_separator()
        
        test_comprehensive_legacy_code()
        print_separator()
        
        test_modern_code()
        print_separator()
        
        print("✅ All tests completed successfully!")
        print("\n💡 Run full test suite with: pytest backend/tests/")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
