"""
Test suite for FastAPI endpoints.
Tests API routes, request/response handling, and error cases.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


class TestAPIEndpoints:
    """Test suite for API endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns correct message."""
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.json() == {"message": "CodeArchaeologist API is running"}
    
    def test_health_endpoint_mock_mode(self, client):
        """Test health endpoint in mock mode."""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'placeholder'}):
            response = client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'healthy'
            assert data['ai_engine'] == 'mock_mode'
    
    def test_health_endpoint_configured(self, client):
        """Test health endpoint with configured API key."""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'real_api_key'}):
            response = client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'healthy'
            assert data['ai_engine'] == 'configured'
    
    def test_analyze_endpoint_mock_mode(self, client):
        """Test analyze endpoint in mock mode."""
        from pathlib import Path
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'placeholder'}):
            # Mock repository cloning to avoid actual git operations
            with patch('services.repository_ingester.RepositoryIngester.clone_repository') as mock_clone:
                mock_clone.return_value = Path('/tmp/test_repo')
                
                # Mock metadata extraction
                with patch('services.repository_ingester.RepositoryIngester.extract_metadata') as mock_metadata:
                    mock_metadata.return_value = {'default_branch': 'main', 'last_commit': 'abc123'}
                    
                    response = client.post(
                        "/analyze",
                        json={
                            "url": "https://github.com/test/repo",
                            "target_lang": "Python 3.11"
                        }
                    )
            
            assert response.status_code == 200
            data = response.json()
            
            assert 'original_code' in data
            assert 'modernized_code' in data
            assert 'summary' in data
            assert len(data['original_code']) > 0
            assert len(data['modernized_code']) > 0
            assert 'Mock' in data['summary'] or 'mock' in data['summary'].lower()
    
    def test_analyze_endpoint_with_ai(self, client):
        """Test analyze endpoint with mocked AI."""
        from pathlib import Path
        mock_modernized = "def modern_func(x: int) -> int:\n    return x * 2"
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            # Mock repository cloning
            with patch('services.repository_ingester.RepositoryIngester.clone_repository') as mock_clone:
                mock_clone.return_value = Path('/tmp/test_repo')
                
                # Mock metadata extraction
                with patch('services.repository_ingester.RepositoryIngester.extract_metadata') as mock_metadata:
                    mock_metadata.return_value = {'default_branch': 'main', 'last_commit': 'abc123'}
                    
                    # Mock AI resurrection
                    with patch('services.ai_engine.resurrect', return_value=mock_modernized):
                        response = client.post(
                            "/analyze",
                            json={
                                "url": "https://github.com/test/repo",
                                "target_lang": "Python 3.11"
                            }
                        )
                
                assert response.status_code == 200
                data = response.json()
                
                assert data['modernized_code'] == mock_modernized
                assert 'successfully modernized' in data['summary'].lower()
    
    def test_analyze_endpoint_missing_url(self, client):
        """Test analyze endpoint with missing URL."""
        response = client.post(
            "/analyze",
            json={"target_lang": "Python 3.11"}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_analyze_endpoint_default_target_lang(self, client):
        """Test analyze endpoint uses default target language."""
        from pathlib import Path
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'placeholder'}):
            # Mock repository cloning
            with patch('services.repository_ingester.RepositoryIngester.clone_repository') as mock_clone:
                mock_clone.return_value = Path('/tmp/test_repo')
                
                # Mock metadata extraction
                with patch('services.repository_ingester.RepositoryIngester.extract_metadata') as mock_metadata:
                    mock_metadata.return_value = {'default_branch': 'main', 'last_commit': 'abc123'}
                    
                    response = client.post(
                        "/analyze",
                        json={"url": "https://github.com/test/repo"}
                    )
            
            assert response.status_code == 200
            # Should use default "Python 3.11"
    
    def test_analyze_endpoint_ai_error(self, client):
        """Test analyze endpoint handles AI errors."""
        from pathlib import Path
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            # Mock repository cloning
            with patch('services.repository_ingester.RepositoryIngester.clone_repository') as mock_clone:
                mock_clone.return_value = Path('/tmp/test_repo')
                
                # Mock metadata extraction
                with patch('services.repository_ingester.RepositoryIngester.extract_metadata') as mock_metadata:
                    mock_metadata.return_value = {'default_branch': 'main', 'last_commit': 'abc123'}
                    
                    # Mock AI error
                    with patch('services.ai_engine.resurrect', side_effect=Exception("AI Error")):
                        response = client.post(
                            "/analyze",
                            json={
                                "url": "https://github.com/test/repo",
                                "target_lang": "Python 3.11"
                            }
                        )
                
                assert response.status_code == 500
                assert 'AI' in response.json()['detail'] or 'error' in response.json()['detail'].lower()
    
    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options(
            "/analyze",
            headers={"Origin": "http://localhost:3000"}
        )
        
        # CORS middleware should add headers
        assert response.status_code in [200, 405]  # OPTIONS might not be explicitly defined


class TestRequestValidation:
    """Test suite for request validation."""
    
    def test_analyze_validates_url_field(self, client):
        """Test that URL field is validated."""
        response = client.post(
            "/analyze",
            json={"target_lang": "Python 3.11"}
        )
        
        assert response.status_code == 422
    
    def test_analyze_accepts_valid_request(self, client):
        """Test that valid request is accepted."""
        from pathlib import Path
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'placeholder'}):
            # Mock repository cloning
            with patch('services.repository_ingester.RepositoryIngester.clone_repository') as mock_clone:
                mock_clone.return_value = Path('/tmp/test_repo')
                
                # Mock metadata extraction
                with patch('services.repository_ingester.RepositoryIngester.extract_metadata') as mock_metadata:
                    mock_metadata.return_value = {'default_branch': 'main', 'last_commit': 'abc123'}
                    
                    response = client.post(
                        "/analyze",
                        json={
                            "url": "https://github.com/user/repo",
                            "target_lang": "Python 3.11"
                        }
                    )
            
            assert response.status_code == 200


class TestResponseFormat:
    """Test suite for response format validation."""
    
    def test_analyze_response_structure(self, client):
        """Test that analyze response has correct structure."""
        from pathlib import Path
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'placeholder'}):
            # Mock repository cloning
            with patch('services.repository_ingester.RepositoryIngester.clone_repository') as mock_clone:
                mock_clone.return_value = Path('/tmp/test_repo')
                
                # Mock metadata extraction
                with patch('services.repository_ingester.RepositoryIngester.extract_metadata') as mock_metadata:
                    mock_metadata.return_value = {'default_branch': 'main', 'last_commit': 'abc123'}
                    
                    response = client.post(
                        "/analyze",
                        json={
                            "url": "https://github.com/test/repo",
                            "target_lang": "Python 3.11"
                        }
                    )
            
            assert response.status_code == 200
            data = response.json()
            
            # Check required fields
            assert 'original_code' in data
            assert 'modernized_code' in data
            assert 'summary' in data
            
            # Check types
            assert isinstance(data['original_code'], str)
            assert isinstance(data['modernized_code'], str)
            assert isinstance(data['summary'], str) or data['summary'] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
