# ✅ Setup Checklist

Use this checklist to set up CodeArchaeologist step by step.

---

## 📋 Pre-Setup

- [ ] Python 3.11+ installed (`python --version`)
- [ ] Node.js 20+ installed (`node --version`)
- [ ] Git installed (`git --version`)
- [ ] Code editor ready (VS Code recommended)

---

## 🗄️ Database Setup

- [ ] Created Neon account at https://console.neon.tech/
- [ ] Created new project named "codearchaeologist"
- [ ] Created database named "codearchaeologist"
- [ ] Copied connection string
- [ ] Modified connection string to use `/codearchaeologist` database

**Connection string format:**
```
postgresql://user:pass@ep-xxx.region.aws.neon.tech/codearchaeologist?sslmode=require
```

---

## 🔑 API Keys

- [ ] Got Gemini API key from https://makersuite.google.com/app/apikey
- [ ] Got GitHub token from https://github.com/settings/tokens (optional)
  - [ ] Selected `repo` scope for private repos
  - [ ] Or selected `public_repo` for public repos only

---

## 🔧 Backend Setup

- [ ] Navigated to backend directory: `cd backend`
- [ ] Created virtual environment: `python -m venv venv`
- [ ] Activated virtual environment:
  - Windows: `venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Copied .env file: `cp .env.example .env`
- [ ] Edited `.env` file with:
  - [ ] GEMINI_API_KEY
  - [ ] DATABASE_URL
  - [ ] GITHUB_TOKEN (optional)
- [ ] Ran database setup: `python setup_database.py`
- [ ] Saw success message: "✅ Database setup complete!"

---

## 🎨 Frontend Setup

- [ ] Navigated to frontend directory: `cd frontend`
- [ ] Installed dependencies: `npm install`
- [ ] (Optional) Copied .env: `cp .env.example .env`

---

## 🚀 First Run

### Terminal 1 - Backend
- [ ] Activated venv: `source venv/bin/activate`
- [ ] Started server: `uvicorn main:app --reload`
- [ ] Saw: "✅ Database connection successful"
- [ ] Server running on http://0.0.0.0:8000

### Terminal 2 - Frontend
- [ ] Started dev server: `npm run dev`
- [ ] Server running on http://localhost:3000

---

## 🧪 Verification

- [ ] Opened http://localhost:8000/health
- [ ] Saw:
  ```json
  {
    "status": "healthy",
    "ai_engine": "configured",
    "database": "connected"
  }
  ```
- [ ] Opened http://localhost:8000/docs
- [ ] Saw interactive API documentation
- [ ] Opened http://localhost:3000
- [ ] Saw CodeArchaeologist dashboard

---

## 🎯 First Test

- [ ] Entered repository URL: `https://github.com/pallets/flask`
- [ ] Clicked "Resurrect" button
- [ ] Watched backend terminal logs
- [ ] Saw: "Successfully cloned repository"
- [ ] Checked `backend/temp_repos/` directory
- [ ] Found cloned repository folder
- [ ] Opened http://localhost:8000/api/repositories
- [ ] Saw repository in list

---

## 🗄️ Database Verification

- [ ] Opened Neon Console: https://console.neon.tech/
- [ ] Navigated to SQL Editor
- [ ] Ran query:
  ```sql
  SELECT id, name, status, created_at FROM repositories;
  ```
- [ ] Saw cloned repository in results

---

## 🐛 Troubleshooting (if needed)

### Database Connection Failed
- [ ] Checked DATABASE_URL in `.env`
- [ ] Verified database name is `codearchaeologist`
- [ ] Checked Neon Console - database is running
- [ ] Tried re-running: `python setup_database.py`

### Module Not Found
- [ ] Verified virtual environment is activated
- [ ] Re-ran: `pip install -r requirements.txt`
- [ ] Checked Python version: `python --version`

### Port Already in Use
- [ ] Killed process on port 8000
- [ ] Or used different port: `uvicorn main:app --reload --port 8001`

### Repository Clone Failed
- [ ] Checked repository URL is valid
- [ ] Verified internet connection
- [ ] For private repos, checked GITHUB_TOKEN is set
- [ ] Verified Git is installed: `git --version`

---

## ✅ Setup Complete!

If all items are checked, you're ready to go! 🎉

### What You Can Do Now:

1. **Analyze Repositories**
   - Enter any public GitHub URL
   - Watch it clone and analyze
   - View results in database

2. **Explore API**
   - Visit http://localhost:8000/docs
   - Try different endpoints
   - See interactive documentation

3. **Check Database**
   - Open Neon Console
   - Query your data
   - See stored repositories

4. **Next Steps**
   - Read IMPROVEMENT_TASKS.md
   - Implement multi-file analysis
   - Add property-based tests
   - Enhance frontend

---

## 📚 Reference Documents

- **QUICK_START.md** - 5-minute setup guide
- **SETUP_GUIDE.md** - Detailed setup instructions
- **IMPROVEMENT_TASKS.md** - What to build next
- **IMPLEMENTATION_SUMMARY.md** - What we built

---

## 🆘 Still Having Issues?

1. Check backend terminal for error messages
2. Check frontend terminal for errors
3. Visit http://localhost:8000/health
4. Review SETUP_GUIDE.md troubleshooting section
5. Check that all environment variables are set correctly

---

**Happy coding! 🏛️⚡**
