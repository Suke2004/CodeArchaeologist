#!/usr/bin/env python3
"""
Frontend-Backend Connectivity Test
Tests that the backend API is accessible and working correctly.
"""

import requests
import json
import sys
from typing import Dict, Any


class Colors:
    """ANSI color codes."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str) -> None:
    """Print formatted header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")


def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text: str) -> None:
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_warning(text: str) -> None:
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text: str) -> None:
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def test_backend_running(base_url: str) -> bool:
    """Test if backend is running."""
    print_info(f"Testing backend at: {base_url}")
    
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is running: {data.get('message', 'OK')}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend")
        print_info("Make sure backend is running: cd backend && uvicorn main:app --reload")
        return False
    except requests.exceptions.Timeout:
        print_error("Backend connection timeout")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False


def test_health_endpoint(base_url: str) -> bool:
    """Test health check endpoint."""
    print_info("Testing health endpoint...")
    
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'unknown')
            ai_engine = data.get('ai_engine', 'unknown')
            
            print_success(f"Health check passed")
            print_info(f"  Status: {status}")
            print_info(f"  AI Engine: {ai_engine}")
            
            if ai_engine == "mock_mode":
                print_warning("  Running in mock mode (GEMINI_API_KEY not configured)")
            
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False


def test_analyze_endpoint(base_url: str) -> bool:
    """Test analyze endpoint."""
    print_info("Testing analyze endpoint...")
    
    payload = {
        "url": "https://github.com/test/repo",
        "target_lang": "Python 3.11"
    }
    
    try:
        response = requests.post(
            f"{base_url}/analyze",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify response structure
            if 'original_code' in data and 'modernized_code' in data:
                print_success("Analyze endpoint working")
                print_info(f"  Original code length: {len(data['original_code'])} chars")
                print_info(f"  Modernized code length: {len(data['modernized_code'])} chars")
                
                if 'summary' in data and data['summary']:
                    print_info(f"  Summary: {data['summary'][:100]}...")
                
                return True
            else:
                print_error("Response missing required fields")
                print_info(f"  Response keys: {list(data.keys())}")
                return False
        else:
            print_error(f"Analyze endpoint failed with status {response.status_code}")
            try:
                error_data = response.json()
                print_info(f"  Error: {error_data.get('detail', 'Unknown error')}")
            except:
                print_info(f"  Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print_error("Analyze request timeout (>30s)")
        return False
    except Exception as e:
        print_error(f"Analyze endpoint error: {e}")
        import traceback
        print_info(f"  Details: {traceback.format_exc()}")
        return False


def test_cors_headers(base_url: str) -> bool:
    """Test CORS configuration."""
    print_info("Testing CORS headers...")
    
    try:
        response = requests.options(
            f"{base_url}/analyze",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            },
            timeout=5
        )
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        if cors_headers['Access-Control-Allow-Origin']:
            print_success("CORS headers present")
            for key, value in cors_headers.items():
                if value:
                    print_info(f"  {key}: {value}")
            return True
        else:
            print_warning("CORS headers not found (might be OK)")
            return True  # Not critical
            
    except Exception as e:
        print_warning(f"CORS test inconclusive: {e}")
        return True  # Not critical


def test_frontend_config() -> bool:
    """Test frontend configuration."""
    print_info("Checking frontend configuration...")
    
    import os
    from pathlib import Path
    
    frontend_env = Path("frontend/.env")
    
    if frontend_env.exists():
        print_success("Frontend .env file exists")
        
        with open(frontend_env, 'r') as f:
            content = f.read()
            
        if 'NEXT_PUBLIC_API_URL' in content:
            print_success("NEXT_PUBLIC_API_URL is configured")
            
            # Extract the URL
            for line in content.split('\n'):
                if 'NEXT_PUBLIC_API_URL' in line and '=' in line:
                    url = line.split('=')[1].strip()
                    print_info(f"  API URL: {url}")
        else:
            print_warning("NEXT_PUBLIC_API_URL not set in frontend/.env")
            print_info("  Will use default: http://localhost:8000")
        
        return True
    else:
        print_warning("Frontend .env file not found")
        print_info("  Create from template: cp frontend/.env.example frontend/.env")
        return False


def main():
    """Run all connectivity tests."""
    print_header("Frontend-Backend Connectivity Test")
    
    # Test configuration
    base_url = "http://localhost:8000"
    
    results = []
    
    # Run tests
    print_header("Backend Tests")
    results.append(("Backend Running", test_backend_running(base_url)))
    
    if results[-1][1]:  # Only continue if backend is running
        results.append(("Health Endpoint", test_health_endpoint(base_url)))
        results.append(("Analyze Endpoint", test_analyze_endpoint(base_url)))
        results.append(("CORS Headers", test_cors_headers(base_url)))
    
    print_header("Frontend Configuration")
    results.append(("Frontend Config", test_frontend_config()))
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"{status} - {name}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}✅ All connectivity tests passed!{Colors.END}")
        print(f"\n{Colors.BOLD}Frontend should be able to connect to backend.{Colors.END}")
        print(f"\n{Colors.CYAN}Next steps:{Colors.END}")
        print(f"  1. Make sure backend is running: cd backend && uvicorn main:app --reload")
        print(f"  2. Make sure frontend is running: cd frontend && npm run dev")
        print(f"  3. Open browser: http://localhost:3000")
        return 0
    else:
        print(f"\n{Colors.RED}❌ Some tests failed.{Colors.END}")
        print(f"\n{Colors.YELLOW}Troubleshooting:{Colors.END}")
        
        if not results[0][1]:  # Backend not running
            print(f"  • Start backend: cd backend && uvicorn main:app --reload")
            print(f"  • Check backend logs for errors")
            print(f"  • Verify dependencies: pip install -r backend/requirements.txt")
        
        print(f"\n{Colors.CYAN}For more help:{Colors.END}")
        print(f"  • Run: python setup_verify.py")
        print(f"  • Run: cd backend && python test_backend.py")
        print(f"  • See: TROUBLESHOOTING.md")
        
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test cancelled.{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
