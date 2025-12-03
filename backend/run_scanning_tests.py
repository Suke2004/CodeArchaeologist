#!/usr/bin/env python
"""
Simple script to run file scanning property tests.
This can be run directly without pytest if needed.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run the file scanning property tests."""
    import pytest
    
    print("=" * 70)
    print("Running File Scanning Property Tests")
    print("=" * 70)
    print()
    
    # Run pytest with specific options
    test_file = os.path.join(os.path.dirname(__file__), "tests", "test_properties_scanning.py")
    args = [
        test_file,
        "-v",
        "--tb=short",
        "--hypothesis-show-statistics",
    ]
    
    exit_code = pytest.main(args)
    
    print()
    print("=" * 70)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. See output above for details.")
    print("=" * 70)
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
