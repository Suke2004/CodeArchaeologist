# 🚀 Quick Start - CodeArchaeologist

**Get up and running in 5 minutes!**

---

## ⚡ Super Quick Setup

### 1. Get Your Credentials (2 minutes)

**Neon Postgres:**
1. Go to https://console.neon.tech/
2. Create project → Copy connection string
3. Change `neondb` to `codearchaeologist` in the URL

**Gemini API:**
1. Go to https://makersuite.google.com/app/apikey
2. Create API key → Copy it

**GitHub Token (optional):**
1. Go to https://github.com/settings/tokens
2. Generate new token (classic) → Select `repo` scope → Copy it

### 2. Install Dependencies (1 minute)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend (in another terminal)
cd frontend
npm install
```

### 3. Configure Environment (1 minute)

```bash
# Backend
cd backend
cp .env.example .env
# Edit .env and paste your credentials
```

**Your .env should look like:**
```env
GEMINI_API_KEY=AIzaSy...your_key_here
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/codearchaeologist?sslmode=require
GITHUB_TOKEN=ghp_...your_token_here
```

### 4. Initialize Database (30 seconds)

```bash
cd backend
python setup_database.py
```

Should see: `✅ Database setup complete!`

### 5. Start Everything (30 seconds)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 6. Test It! (30 seconds)

1. Open http://localhost:3000
2. Enter: `https://github.com/pallets/flask`
3. Click "Resurrect"
4. Watch it clone and analyze! 🎉

---

## 🎯 What You Just Built

✅ **Database** - Neon Postgres storing all data  
✅ **Repository Cloning** - Real GitHub repos  
✅ **AI Analysis** - Gemini-powered modernization  
✅ **API** - RESTful endpoints  
✅ **Frontend** - Beautiful dashboard  

---

## 📝 Quick Commands

```bash
# Check if everything is working
curl http://localhost:8000/health

# List analyzed repositories
curl http://localhost:8000/api/repositories

# View API docs
open http://localhost:8000/docs

# Run tests
cd backend && pytest
```

---

## 🐛 Quick Fixes

**Database connection failed?**
```bash
# Check your DATABASE_URL in backend/.env
# Make sure it ends with /codearchaeologist?sslmode=require
```

**Module not found?**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Port already in use?**
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

---

## 📚 Next Steps

1. **Read SETUP_GUIDE.md** - Detailed setup instructions
2. **Read IMPROVEMENT_TASKS.md** - See what to build next
3. **Check backend/temp_repos/** - See cloned repositories
4. **Query Neon Console** - View your data in SQL Editor

---

## 🆘 Need Help?

- **Health Check:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs
- **Backend Logs:** Check terminal running uvicorn
- **Frontend Logs:** Check terminal running npm dev

---

**You're all set! Start resurrecting some legacy code! 🏛️⚡**
