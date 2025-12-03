# Troubleshooting Guide

Common issues and solutions for CodeArchaeologist.

## Quick Diagnostics

```bash
# Run comprehensive checks
python setup_verify.py

# Test backend
cd backend
python test_backend.py

# Run tests
pytest
```

## Common Issues

### 1. HTTP 500 Error When Analyzing Code

**Symptoms:**
- Frontend shows "Error: HTTP error! status: 500"
- Terminal logs show error messages

**Solutions:**

**A. Check Backend Logs**
Look at the terminal running `uvicorn main:app --reload` for error details.

**B. Test the Detector**
```bash
cd backend
python test_backend.py
```

**C. Verify Dependencies**
```bash
pip install -r requirements.txt
```

**D. Check Environment**
```bash
# Verify .env file exists
ls -la backend/.env

# Check API key is set
cat backend/.env | grep GEMINI_API_KEY
```

**E. Test Manually**
```bash
cd backend
python -c "from services.legacy_detector import LegacyDetector; d = LegacyDetector(); print('OK')"
```

### 2. Backend Won't Start

**Symptoms:**
- `uvicorn main:app --reload` fails
- Import errors
- Module not found errors

**Solutions:**

**A. Check Python Version**
```bash
python --version
# Should be 3.11 or higher
```

**B. Verify Virtual Environment**
```bash
cd backend

# Create if missing
python -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

**C. Check PYTHONPATH**
```bash
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn main:app --reload
```

**D. Test Imports**
```bash
python -c "import fastapi; print('FastAPI OK')"
python -c "import pydantic; print('Pydantic OK')"
python -c "from services.legacy_detector import LegacyDetector; print('Detector OK')"
```

### 3. Frontend Connection Error

**Symptoms:**
- Frontend can't connect to backend
- CORS errors in browser console
- Network errors

**Solutions:**

**A. Verify Backend is Running**
```bash
curl http://localhost:8000/
# Should return: {"message":"CodeArchaeologist API is running"}

curl http://localhost:8000/health
# Should return: {"status":"healthy","ai_engine":"mock_mode"}
```

**B. Check CORS Configuration**
Edit `backend/main.py` and verify:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Must match frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**C. Check Ports**
```bash
# Backend should be on 8000
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Frontend should be on 3000
lsof -i :3000  # Linux/macOS
netstat -ano | findstr :3000  # Windows
```

**D. Try Different Port**
```bash
# Backend
uvicorn main:app --reload --port 8001

# Frontend
npm run dev -- --port 3001

# Update CORS in backend/main.py to match
```

### 4. Tests Failing

**Symptoms:**
- `pytest` shows failures
- Import errors in tests
- Assertion errors

**Solutions:**

**A. Run with Verbose Output**
```bash
cd backend
pytest -v --tb=long
```

**B. Run Specific Test**
```bash
pytest tests/test_legacy_detector.py::TestLegacyDetector::test_detect_eval_usage -v
```

**C. Check Test Dependencies**
```bash
pip install pytest pytest-asyncio pytest-cov
```

**D. Verify Test Files**
```bash
ls -la backend/tests/
# Should see: test_legacy_detector.py, test_api.py, test_ai_engine.py
```

**E. Clear Cache**
```bash
cd backend
rm -rf .pytest_cache __pycache__ tests/__pycache__
pytest
```

### 5. Import Errors

**Symptoms:**
- `ModuleNotFoundError`
- `ImportError`
- Can't find services module

**Solutions:**

**A. Check Directory Structure**
```bash
cd backend
ls -la services/
# Should see: __init__.py, legacy_detector.py, ai_engine.py
```

**B. Verify __init__.py Files**
```bash
# Should exist
ls backend/services/__init__.py
ls backend/tests/__init__.py
```

**C. Add to PYTHONPATH**
```bash
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**D. Run from Correct Directory**
```bash
# Always run from backend directory
cd backend
pytest
python test_detector.py
uvicorn main:app --reload
```

### 6. API Key Issues

**Symptoms:**
- "GEMINI_API_KEY not configured" error
- AI features not working
- Mock mode always active

**Solutions:**

**A. Check .env File**
```bash
cat backend/.env
# Should contain: GEMINI_API_KEY=your_actual_key
```

**B. Verify Key is Not Placeholder**
```bash
grep GEMINI_API_KEY backend/.env
# Should NOT be: GEMINI_API_KEY=placeholder
```

**C. Generate New Key**
1. Visit: https://makersuite.google.com/app/apikey
2. Create new API key
3. Add to `backend/.env`:
   ```
   GEMINI_API_KEY=AIza...your_key_here
   ```

**D. Restart Backend**
```bash
# Stop uvicorn (Ctrl+C)
# Start again
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### 7. MCP Connector Issues

**Symptoms:**
- TypeScript compilation errors
- MCP not working
- GitHub connector fails

**Solutions:**

**A. Install Dependencies**
```bash
cd mcp
npm install
```

**B. Compile TypeScript**
```bash
cd mcp
npm run build
```

**C. Test MCP**
```bash
cd mcp
node test_mcp.js
```

**D. Check Environment**
```bash
cat mcp/.env
# Should contain: GITHUB_TOKEN=your_token (optional)
```

### 8. Permission Errors

**Symptoms:**
- Can't write files
- Permission denied errors
- Can't execute scripts

**Solutions:**

**A. Make Scripts Executable**
```bash
chmod +x setup.sh
chmod +x backend/test_detector.py
chmod +x backend/test_backend.py
```

**B. Check File Ownership**
```bash
ls -la
# Files should be owned by your user
```

**C. Run with Correct Permissions**
```bash
# Don't use sudo unless necessary
# Use virtual environment instead
```

### 9. Port Already in Use

**Symptoms:**
- "Address already in use" error
- Can't start backend/frontend
- Port conflict

**Solutions:**

**A. Find Process Using Port**
```bash
# Linux/macOS
lsof -i :8000
lsof -i :3000

# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

**B. Kill Process**
```bash
# Linux/macOS
kill -9 <PID>

# Windows
taskkill /PID <PID> /F
```

**C. Use Different Port**
```bash
# Backend
uvicorn main:app --reload --port 8001

# Frontend
npm run dev -- --port 3001
```

### 10. Dependencies Out of Sync

**Symptoms:**
- Version conflicts
- Incompatible packages
- Import errors after update

**Solutions:**

**A. Reinstall Backend Dependencies**
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**B. Reinstall Frontend Dependencies**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**C. Update All Dependencies**
```bash
# Backend
cd backend
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
npm update
```

## Platform-Specific Issues

### Windows

**Issue: Scripts won't run**
```bash
# Use .bat files
setup.bat

# Or use PowerShell
powershell -ExecutionPolicy Bypass -File setup.sh
```

**Issue: Virtual environment activation**
```bash
# Use Windows path
backend\venv\Scripts\activate
```

**Issue: Path separators**
```bash
# Use backslashes or forward slashes
cd backend\tests
cd backend/tests  # Also works
```

### macOS

**Issue: Python version**
```bash
# Use python3 explicitly
python3 --version
python3 -m venv venv
```

**Issue: Permission denied**
```bash
# Make scripts executable
chmod +x setup.sh
./setup.sh
```

### Linux

**Issue: Missing system dependencies**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv nodejs npm

# Fedora/RHEL
sudo dnf install python3.11 nodejs npm
```

## Getting More Help

### 1. Check Logs

**Backend Logs:**
- Terminal running `uvicorn main:app --reload`
- Look for stack traces and error messages

**Frontend Logs:**
- Browser console (F12 → Console tab)
- Terminal running `npm run dev`

### 2. Run Diagnostics

```bash
# Comprehensive check
python setup_verify.py

# Backend test
cd backend
python test_backend.py

# Full test suite
cd backend
pytest -v
```

### 3. Check Documentation

- `README.md` - Project overview
- `TESTING.md` - Testing guide
- `SECURITY.md` - Security policy
- `CONTRIBUTING.md` - Development guide

### 4. Common Commands

```bash
# Setup
./setup.sh  # or setup.bat

# Verify
python setup_verify.py

# Test
cd backend && pytest

# Start
cd backend && uvicorn main:app --reload
cd frontend && npm run dev

# Clean
rm -rf backend/__pycache__ backend/.pytest_cache
rm -rf frontend/.next frontend/node_modules
```

### 5. Reset Everything

If all else fails, start fresh:

```bash
# Backup your .env files
cp backend/.env backend/.env.backup
cp frontend/.env frontend/.env.backup

# Clean everything
rm -rf backend/venv backend/__pycache__ backend/.pytest_cache
rm -rf frontend/node_modules frontend/.next
rm -rf mcp/node_modules

# Run setup again
./setup.sh  # or setup.bat

# Restore .env files
cp backend/.env.backup backend/.env
cp frontend/.env.backup frontend/.env

# Verify
python setup_verify.py
```

## Still Having Issues?

1. **Check existing issues** on GitHub
2. **Search documentation** for keywords
3. **Run diagnostics** with `setup_verify.py`
4. **Open a new issue** with:
   - Error message
   - Steps to reproduce
   - Output of `setup_verify.py`
   - OS and versions (Python, Node.js)

---

**Remember:** Most issues are related to:
- Missing dependencies
- Wrong directory
- Environment not activated
- API keys not configured
- Port conflicts

Run `python setup_verify.py` to check everything!
