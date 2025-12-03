"""
Test suite for AI engine integration.
Tests Gemini API integration and code modernization.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from services.ai_engine import resurrect, analyze_repository


class TestAIEngine:
    """Test suite for AI engine functionality."""
    
    @pytest.mark.asyncio
    async def test_resurrect_without_api_key(self):
        """Test that resurrect raises error without API key."""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'placeholder'}):
            with pytest.raises(ValueError, match="GEMINI_API_KEY not configured"):
                await resurrect("print 'test'", "Python 3.11")
    
    @pytest.mark.asyncio
    async def test_resurrect_with_empty_api_key(self):
        """Test that resurrect raises error with empty API key."""
        with patch.dict(os.environ, {'GEMINI_API_KEY': ''}):
            with pytest.raises(ValueError, match="GEMINI_API_KEY not configured"):
                await resurrect("print 'test'", "Python 3.11")
    
    @pytest.mark.asyncio
    async def test_resurrect_with_valid_api_key(self):
        """Test resurrect with mocked Gemini API."""
        mock_response = MagicMock()
        mock_response.text = """def modern_function(x: int) -> int:
    return x * 2"""
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with patch('services.ai_engine.genai.configure'):
                with patch('services.ai_engine.genai.GenerativeModel', return_value=mock_model):
                    result = await resurrect("def old_func(x): return x * 2", "Python 3.11")
                    
                    assert "def modern_function" in result
                    assert "int" in result
    
    @pytest.mark.asyncio
    async def test_resurrect_removes_markdown_code_blocks(self):
        """Test that markdown code blocks are removed from response."""
        mock_response = MagicMock()
        mock_response.text = """```python
def modern_function(x: int) -> int:
    return x * 2
```"""
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with patch('services.ai_engine.genai.configure'):
                with patch('services.ai_engine.genai.GenerativeModel', return_value=mock_model):
                    result = await resurrect("old code", "Python 3.11")
                    
                    assert not result.startswith("```")
                    assert not result.endswith("```")
                    assert "def modern_function" in result
    
    @pytest.mark.asyncio
    async def test_resurrect_handles_empty_response(self):
        """Test handling of empty AI response."""
        mock_response = MagicMock()
        mock_response.text = ""
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with patch('services.ai_engine.genai.configure'):
                with patch('services.ai_engine.genai.GenerativeModel', return_value=mock_model):
                    with pytest.raises(Exception, match="Empty response from AI model"):
                        await resurrect("old code", "Python 3.11")
    
    @pytest.mark.asyncio
    async def test_resurrect_handles_none_response(self):
        """Test handling of None AI response."""
        mock_model = MagicMock()
        mock_model.generate_content.return_value = None
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with patch('services.ai_engine.genai.configure'):
                with patch('services.ai_engine.genai.GenerativeModel', return_value=mock_model):
                    with pytest.raises(Exception, match="Empty response from AI model"):
                        await resurrect("old code", "Python 3.11")
    
    @pytest.mark.asyncio
    async def test_resurrect_handles_api_error(self):
        """Test handling of API errors."""
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with patch('services.ai_engine.genai.configure'):
                with patch('services.ai_engine.genai.GenerativeModel', return_value=mock_model):
                    with pytest.raises(Exception, match="AI processing failed"):
                        await resurrect("old code", "Python 3.11")
    
    @pytest.mark.asyncio
    async def test_analyze_repository_not_implemented(self):
        """Test that analyze_repository returns not implemented status."""
        result = await analyze_repository("https://github.com/user/repo")
        
        assert result['status'] == 'not_implemented'
        assert 'message' in result


class TestPromptGeneration:
    """Test suite for AI prompt generation."""
    
    @pytest.mark.asyncio
    async def test_prompt_includes_target_language(self):
        """Test that prompt includes target language."""
        mock_response = MagicMock()
        mock_response.text = "modernized code"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with patch('services.ai_engine.genai.configure'):
                with patch('services.ai_engine.genai.GenerativeModel', return_value=mock_model) as mock_gen:
                    await resurrect("old code", "TypeScript 5")
                    
                    # Check that generate_content was called
                    assert mock_model.generate_content.called
                    call_args = mock_model.generate_content.call_args[0][0]
                    assert "TypeScript 5" in call_args
    
    @pytest.mark.asyncio
    async def test_prompt_includes_original_code(self):
        """Test that prompt includes original code."""
        mock_response = MagicMock()
        mock_response.text = "modernized code"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        
        original_code = "print 'Hello, World!'"
        
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            with patch('services.ai_engine.genai.configure'):
                with patch('services.ai_engine.genai.GenerativeModel', return_value=mock_model):
                    await resurrect(original_code, "Python 3.11")
                    
                    call_args = mock_model.generate_content.call_args[0][0]
                    assert original_code in call_args


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
