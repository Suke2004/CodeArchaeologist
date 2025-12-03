# CodeArchaeologist Setup Guide

Complete setup instructions for getting CodeArchaeologist running with Neon Postgres, real repository cloning, and GitHub integration.

---

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Python 3.11+ installed
- ✅ Node.js 20+ installed
- ✅ Git installed
- ✅ A Neon Postgres account (free tier works!)
- ✅ A Google Gemini API key
- ✅ A GitHub personal access token (optional, for private repos)

---

## 🗄️ Step 1: Set Up Neon Postgres Database

### 1.1 Create Neon Database

1. Go to [Neon Console](https://console.neon.tech/)
2. Click "Create Project"
3. Name your project: `codearchaeologist`
4. Select region closest to you
5. Click "Create Project"

### 1.2 Get Connection String

1. In your Neon project dashboard, click "Connection Details"
2. Copy the connection string (it looks like this):
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/neondb?sslmode=require
   ```
3. **Important:** Change the database name from `neondb` to `codearchaeologist`:
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/codearchaeologist?sslmode=require
   ```

### 1.3 Create Database (if needed)

If the database doesn't exist, create it:

1. Go to Neon Console → SQL Editor
2. Run:
   ```sql
   CREATE DATABASE codearchaeologist;
   ```

---

## 🔧 Step 2: Configure Backend

### 2.1 Install Python Dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Create Environment File

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your favorite editor
```

### 2.3 Configure .env File

Open `backend/.env` and add your credentials:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Database Configuration - PASTE YOUR NEON CONNECTION STRING HERE
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/codearchaeologist?sslmode=require

# GitHub Configuration (optional, for private repos)
GITHUB_TOKEN=your_github_token_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000
```

**Where to get credentials:**

- **GEMINI_API_KEY**: https://makersuite.google.com/app/apikey
- **DATABASE_URL**: From Neon Console (see Step 1.2)
- **GITHUB_TOKEN**: https://github.com/settings/tokens (optional)
  - Click "Generate new token (classic)"
  - Select scopes: `repo` (for private repos) or `public_repo` (for public only)
  - Generate and copy the token

### 2.4 Initialize Database

Run the setup script to create tables:

```bash
python setup_database.py
```

You should see:
```
✅ Database connection successful!
✅ Database tables created successfully!
📊 Created tables:
  - repositories
  - analysis_results
```

If you see errors, check:
- Your DATABASE_URL is correct
- Your Neon database is running
- You have internet connectivity

---

## 🎨 Step 3: Configure Frontend

### 3.1 Install Dependencies

```bash
cd frontend
npm install
```

### 3.2 Create Environment File (Optional)

```bash
cp .env.example .env
```

The frontend will work without configuration, but you can customize:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 Step 4: Start the Application

### 4.1 Start Backend

Open a terminal:

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     ✅ Database connection successful
```

### 4.2 Start Frontend

Open another terminal:

```bash
cd frontend
npm run dev
```

You should see:
```
  ▲ Next.js 16.0.6
  - Local:        http://localhost:3000
```

### 4.3 Verify Everything Works

1. **Check API Health:**
   - Open: http://localhost:8000/health
   - Should show:
     ```json
     {
       "status": "healthy",
       "ai_engine": "configured",
       "database": "connected"
     }
     ```

2. **Check API Docs:**
   - Open: http://localhost:8000/docs
   - You should see interactive API documentation

3. **Check Frontend:**
   - Open: http://localhost:3000
   - You should see the CodeArchaeologist dashboard

---

## 🧪 Step 5: Test Real Repository Analysis

### 5.1 Test with a Public Repository

1. Go to http://localhost:3000
2. Enter a repository URL, for example:
   ```
   https://github.com/pallets/flask
   ```
3. Click "Resurrect"
4. Watch the terminal logs in the backend
5. You should see:
   ```
   INFO: Created repository record: <uuid>
   INFO: Cloning repository from https://github.com/pallets/flask
   INFO: Successfully cloned repository to backend/temp_repos/<uuid>_flask
   ```

### 5.2 Check Database

Verify the repository was saved:

1. Go to Neon Console → SQL Editor
2. Run:
   ```sql
   SELECT id, name, status, created_at FROM repositories;
   ```
3. You should see your cloned repository!

### 5.3 List Repositories via API

```bash
curl http://localhost:8000/api/repositories
```

You should see a JSON response with your repositories.

---

## 🔍 Step 6: Verify GitHub Integration (Optional)

If you added a GITHUB_TOKEN, test private repository access:

1. Try cloning a private repository you have access to
2. The system should use your token automatically
3. Check backend logs for successful authentication

---

## 🐛 Troubleshooting

### Database Connection Failed

**Error:** `❌ Database connection failed`

**Solutions:**
1. Check your DATABASE_URL in `.env`
2. Verify your Neon database is running (check Neon Console)
3. Make sure you changed `neondb` to `codearchaeologist` in the URL
4. Check if your IP is allowed (Neon allows all IPs by default)

### Repository Cloning Failed

**Error:** `Failed to clone repository`

**Solutions:**
1. Check the repository URL is valid
2. For private repos, ensure GITHUB_TOKEN is set
3. Check your internet connection
4. Verify Git is installed: `git --version`

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'sqlalchemy'`

**Solutions:**
1. Activate virtual environment: `source venv/bin/activate`
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version: `python --version` (should be 3.11+)

### Port Already in Use

**Error:** `Address already in use`

**Solutions:**
1. Kill the process using the port:
   ```bash
   # On Windows:
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # On macOS/Linux:
   lsof -ti:8000 | xargs kill -9
   ```
2. Or use a different port:
   ```bash
   uvicorn main:app --reload --port 8001
   ```

---

## 📊 What's Working Now

After completing this setup, you have:

✅ **Database Persistence**
- Repositories are saved to Neon Postgres
- Analysis results are stored
- Can query historical data

✅ **Real Repository Cloning**
- Clone any public GitHub repository
- Clone private repos with token
- Extract repository metadata

✅ **GitHub Integration**
- Authenticate with personal access token
- Access private repositories
- Extract commit history

✅ **API Endpoints**
- `POST /analyze` - Analyze repository
- `GET /api/repositories` - List all repositories
- `GET /api/repositories/:id` - Get repository details
- `GET /api/repositories/:id/analysis` - Get analysis results
- `GET /health` - Health check

---

## 🎯 Next Steps

Now that the core infrastructure is working, you can:

1. **Implement Multi-File Analysis** (Task 2.2)
   - Scan all files in cloned repository
   - Analyze each file for legacy patterns
   - Aggregate results

2. **Add Property-Based Tests** (Task 3.1-3.6)
   - Install Hypothesis
   - Write property tests for correctness

3. **Implement Background Processing** (Task 4.1-4.5)
   - Set up Celery for async analysis
   - Add task queue management

4. **Enhance Frontend** (Task 5.1-5.7)
   - Display real repository data
   - Add file tree view
   - Implement split view with Monaco Editor

---

## 📚 Useful Commands

### Backend

```bash
# Start server
uvicorn main:app --reload

# Run tests
pytest

# Check database
python setup_database.py

# View logs
tail -f logs/app.log  # if logging to file
```

### Frontend

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Database

```bash
# Connect to Neon via psql (if installed)
psql "postgresql://username:password@ep-xxx.neon.tech/codearchaeologist?sslmode=require"

# Or use Neon Console SQL Editor
# https://console.neon.tech/
```

---

## 🆘 Need Help?

1. **Check logs** - Backend terminal shows detailed error messages
2. **Check health endpoint** - http://localhost:8000/health
3. **Check API docs** - http://localhost:8000/docs
4. **Review this guide** - Make sure you completed all steps
5. **Check IMPROVEMENT_TASKS.md** - For detailed task breakdown

---

## ✅ Setup Complete!

You now have a fully functional CodeArchaeologist with:
- ✅ Neon Postgres database
- ✅ Real repository cloning
- ✅ GitHub integration
- ✅ API endpoints
- ✅ Frontend dashboard

**Time to start analyzing some legacy code!** 🏛️⚡
