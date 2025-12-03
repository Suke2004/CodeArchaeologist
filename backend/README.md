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
