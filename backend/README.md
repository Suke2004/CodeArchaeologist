# CodeArchaeologist Backend

FastAPI server for analyzing and modernizing legacy code repositories.

## ✨ Features

- 🚀 FastAPI with async support
- 🤖 Google Gemini AI integration for code modernization
- 🗄️ Neon Postgres database with SQLAlchemy ORM
- 📦 Real GitHub repository cloning with GitPython
- 🔒 CORS configured for frontend integration
- 📝 Type-safe with Pydantic models
- 🧪 Comprehensive test suite with pytest

## Setup

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
# Copy .env and add your Gemini API key
cp .env .env.local
# Edit .env and replace 'placeholder' with your actual API key
```

4. **Get Gemini API Key:**
- Visit https://makersuite.google.com/app/apikey
- Create a new API key
- Add it to your `.env` file

## Running the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

Server will be available at: http://localhost:8000

## API Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{
  "message": "CodeArchaeologist API is running"
}
```

### `POST /analyze`
Analyze and modernize legacy code.

**Request:**
```json
{
  "url": "https://github.com/user/repo",
  "target_lang": "Python 3.11"
}
```

**Response:**
```json
{
  "original_code": "# Legacy code...",
  "modernized_code": "# Modern code...",
  "summary": "Code successfully modernized using AI"
}
```

### `GET /health`
Check API health and configuration status.

**Response:**
```json
{
  "status": "healthy",
  "ai_engine": "configured"
}
```

## Mock Mode

If `GEMINI_API_KEY` is not configured or set to "placeholder", the API runs in mock mode:
- Returns sample legacy Python 2 code
- Returns sample modernized Python 3 code
- Useful for frontend development and testing

## Project Structure

```
backend/
├── main.py              # FastAPI application and endpoints
├── services/
│   ├── __init__.py
│   └── ai_engine.py     # Gemini AI integration
├── .env                 # Environment configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | `placeholder` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |

## Development

### Testing the API

```bash
# Using curl
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/test/repo", "target_lang": "Python 3.11"}'

# Check health
curl http://localhost:8000/health
```

### Running Tests

#### Unit Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_legacy_detector.py -v
```

#### Property-Based Tests

CodeArchaeologist uses [Hypothesis](https://hypothesis.readthedocs.io/) for property-based testing, which automatically generates hundreds of test cases to verify that system properties hold across all inputs.

**Run property tests:**
```bash
# Run all property tests (100 examples each)
pytest -m property

# Run with verbose output and statistics
pytest -m property --hypothesis-show-statistics -v

# Run specific property test file
pytest tests/test_properties_ingestion.py -v

# Run with increased examples for thorough testing
HYPOTHESIS_MAX_EXAMPLES=1000 pytest -m property
```

**What are Property Tests?**

Property-based tests verify universal behaviors rather than specific examples:
- **Unit Test**: "When I add task 'Buy milk', the list length increases by 1"
- **Property Test**: "For ANY valid task, adding it increases the list length by 1"

Hypothesis generates diverse inputs automatically, finding edge cases you might miss.

**Example Property Test Output:**
```
tests/test_properties_ingestion.py::test_invalid_url_rejection PASSED
  - Hypothesis generated 100 examples
  - Smallest failing example (if any): shown automatically
  - All invalid URLs correctly rejected ✓

tests/test_properties_scanning.py::test_file_statistics_consistency PASSED
  - Tested with 100 different directory structures
  - File counts always sum correctly ✓
```

**Debugging Failed Properties:**

When a property test fails, Hypothesis shows the minimal failing example:

```python
# Example failure output
Falsifying example: test_url_validation(
    url='http://github.com/user/repo.git\x00'  # Contains null byte
)
```

To debug:
1. Copy the failing example from the output
2. Add it as a unit test for regression testing
3. Fix the bug in the code
4. Re-run the property test to verify the fix

**Property Test Categories:**

1. **Repository Ingestion** (`test_properties_ingestion.py`)
   - URL validation across all formats
   - Metadata extraction completeness
   - Error handling consistency

2. **File Scanning** (`test_properties_scanning.py`)
   - File identification across directory structures
   - Ignored directory exclusion
   - Statistics consistency

3. **Dependency Extraction** (`test_properties_extraction.py`)
   - Parsing correctness for all formats
   - Version constraint preservation
   - Malformed file handling

4. **Analysis Completeness** (`test_properties_analysis.py`)
   - Language percentage summation
   - File count consistency
   - Technical debt grade accuracy

5. **Data Persistence** (`test_properties_persistence.py`)
   - Round-trip data preservation
   - Timestamp handling
   - JSON serialization correctness

6. **Generator Validation** (`test_properties_generators.py`)
   - Test data generator correctness
   - Meta-tests for test infrastructure

**Configuration:**

Property test settings are in `pytest.ini`:
```ini
[tool:pytest]
markers =
    property: Property-based tests using Hypothesis

[tool.hypothesis]
max_examples = 100
deadline = 5000
verbosity = normal
```

### API Documentation

FastAPI provides automatic interactive documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Future Enhancements

- [ ] Repository cloning and analysis
- [ ] Multi-file processing
- [ ] Batch processing support
- [ ] Caching for repeated requests
- [ ] Rate limiting
- [ ] Authentication
- [ ] WebSocket support for real-time updates
- [ ] Support for multiple AI providers
