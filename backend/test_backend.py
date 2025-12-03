#!/usr/bin/env python3
"""
Quick backend test script.
Run this to verify the backend is working correctly.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.legacy_detector import LegacyDetector


def test_detector():
    """Test the legacy detector."""
    print("Testing Legacy Detector...")
    
    detector = LegacyDetector()
    
    code = """# Legacy Python 2 code
print "Hello, World!"

def fetch_users(callback):
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
"""
    
    try:
        issues = detector.detect_python_issues(code)
        report = detector.generate_report(issues)
        tech_debt = detector.calculate_tech_debt(issues)
        
        print(f"✅ Detector working!")
        print(f"   Issues found: {report['total_issues']}")
        print(f"   Grade: {tech_debt['grade']}")
        print(f"   Score: {tech_debt['maintainability_score']}/100")
        return True
    except Exception as e:
        print(f"❌ Detector failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_key():
    """Test API key configuration."""
    print("\nTesting API Key Configuration...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("⚠️  GEMINI_API_KEY not set")
        print("   Set in backend/.env for AI features")
        return False
    elif api_key == "placeholder":
        print("⚠️  GEMINI_API_KEY is placeholder")
        print("   Replace with real key for AI features")
        return False
    else:
        print(f"✅ GEMINI_API_KEY configured")
        print(f"   Key: {api_key[:10]}...")
        return True


def test_imports():
    """Test that all imports work."""
    print("\nTesting Imports...")
    
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI not installed: {e}")
        return False
    
    try:
        import pydantic
        print(f"✅ Pydantic {pydantic.__version__}")
    except ImportError as e:
        print(f"❌ Pydantic not installed: {e}")
        return False
    
    try:
        import google.generativeai
        print(f"✅ Google Generative AI installed")
    except ImportError as e:
        print(f"❌ Google Generative AI not installed: {e}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("="*60)
    print("Backend Test Suite")
    print("="*60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Detector", test_detector()))
    results.append(("API Key", test_api_key()))
    
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✅ All tests passed!")
        print("\nBackend is ready to use.")
        print("Start with: uvicorn main:app --reload")
    else:
        print("\n⚠️  Some tests failed.")
        print("Check the errors above and fix them.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
