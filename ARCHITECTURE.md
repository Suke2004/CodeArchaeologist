# CodeArchaeologist Architecture

**Current Implementation Status:** Phase 1 Complete ✅

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    http://localhost:3000                        │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Dashboard  │  │  Code Diff   │  │   Terminal   │        │
│  │    Page      │  │    Viewer    │  │   Component  │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                            │
│                   http://localhost:8000                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    API ENDPOINTS                          │ │
│  │  POST /analyze                                            │ │
│  │  GET  /api/repositories                                   │ │
│  │  GET  /api/repositories/:id                               │ │
│  │  GET  /api/repositories/:id/analysis                      │ │
│  │  GET  /health                                             │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                     SERVICES                              │ │
│  │  ┌────────────────┐  ┌────────────────┐                 │ │
│  │  │ Legacy         │  │ Repository     │                 │ │
│  │  │ Detector       │  │ Ingester       │                 │ │
│  │  │ (30+ rules)    │  │ (GitPython)    │                 │ │
│  │  └────────────────┘  └────────────────┘                 │ │
│  │  ┌────────────────┐  ┌────────────────┐                 │ │
│  │  │ AI Engine      │  │ GitHub         │                 │ │
│  │  │ (Gemini)       │  │ Service        │                 │ │
│  │  └────────────────┘  └────────────────┘                 │ │
│  └──────────────────────────────────────────────────────────┘ │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                  DATABASE MODELS                          │ │
│  │  ┌────────────────┐  ┌────────────────┐                 │ │
│  │  │ LegacyRepo     │  │ AnalysisResult │                 │ │
│  │  │ (SQLAlchemy)   │  │ (SQLAlchemy)   │                 │ │
│  │  └────────────────┘  └────────────────┘                 │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ PostgreSQL Protocol
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │ Neon Postgres    │  │ Local Storage    │                   │
│  │ (Cloud Database) │  │ (temp_repos/)    │                   │
│  │                  │  │                  │                   │
│  │ • repositories   │  │ • Cloned repos   │                   │
│  │ • analysis_results│ │ • Git data       │                   │
│  └──────────────────┘  └──────────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ External APIs
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   GitHub     │  │    Google    │  │     MCP      │        │
│  │     API      │  │    Gemini    │  │  Connector   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Flow

### 1. Repository Analysis Flow

```
User enters URL
      │
      ▼
Frontend sends POST /analyze
      │
      ▼
Backend validates URL
      │
      ▼
Create LegacyRepo record in DB
      │
      ▼
Clone repository with GitPython
      │
      ▼
Extract metadata (commits, size, etc.)
      │
      ▼
Update DB with clone info
      │
      ▼
Analyze code with Legacy Detector
      │
      ▼
Transform code with Gemini AI
      │
      ▼
Create AnalysisResult record in DB
      │
      ▼
Return results to frontend
      │
      ▼
Display in UI
```

### 2. Repository Listing Flow

```
User opens dashboard
      │
      ▼
Frontend sends GET /api/repositories
      │
      ▼
Backend queries DB
      │
      ▼
Return list of LegacyRepo records
      │
      ▼
Frontend displays repository cards
```

---

## 🗄️ Database Schema

### repositories table

```sql
CREATE TABLE repositories (
    id VARCHAR PRIMARY KEY,
    url VARCHAR NOT NULL UNIQUE,
    name VARCHAR NOT NULL,
    owner VARCHAR,
    user_id VARCHAR NOT NULL DEFAULT 'anonymous',
    status VARCHAR NOT NULL,  -- pending, cloning, analyzing, complete, failed
    cloned_at TIMESTAMP,
    storage_path VARCHAR,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### analysis_results table

```sql
CREATE TABLE analysis_results (
    id VARCHAR PRIMARY KEY,
    repo_id VARCHAR NOT NULL REFERENCES repositories(id),
    languages JSONB DEFAULT '[]',
    frameworks JSONB DEFAULT '[]',
    issues JSONB DEFAULT '[]',
    tech_debt JSONB DEFAULT '{}',
    total_files INTEGER DEFAULT 0,
    total_lines INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## 📁 Directory Structure

```
codearchaeologist/
├── backend/
│   ├── models/                    # ✅ Database models
│   │   ├── __init__.py
│   │   ├── base.py               # Base model with timestamps
│   │   ├── repository.py         # LegacyRepo model
│   │   └── analysis.py           # AnalysisResult model
│   │
│   ├── services/                  # ✅ Business logic
│   │   ├── __init__.py
│   │   ├── ai_engine.py          # Gemini AI integration
│   │   ├── legacy_detector.py    # Pattern detection
│   │   └── repository_ingester.py # Repository cloning
│   │
│   ├── tests/                     # ✅ Test suite
│   │   ├── test_ai_engine.py
│   │   ├── test_legacy_detector.py
│   │   └── test_api.py
│   │
│   ├── temp_repos/                # ✅ Cloned repositories
│   │   └── {repo_id}_{repo_name}/
│   │
│   ├── database.py                # ✅ Database connection
│   ├── main.py                    # ✅ FastAPI application
│   ├── setup_database.py          # ✅ Database setup script
│   ├── requirements.txt           # ✅ Python dependencies
│   └── .env                       # ✅ Environment variables
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx              # Main dashboard
│   │   ├── layout.tsx            # Root layout
│   │   └── globals.css           # Styles
│   │
│   ├── components/
│   │   ├── CodeDiff.tsx          # Diff viewer
│   │   └── Terminal.tsx          # Terminal component
│   │
│   └── package.json              # Node dependencies
│
├── mcp/
│   ├── github_connector.ts       # ✅ MCP GitHub integration
│   └── package.json
│
├── .kiro/
│   ├── specs/
│   │   └── code-archaeologist/
│   │       ├── requirements.md
│   │       ├── design.md
│   │       └── tasks.md
│   │
│   └── steering/
│       ├── modernization_standards.md
│       ├── legacy_detection.md
│       └── documentation_style.md
│
└── Documentation/                 # ✅ NEW!
    ├── README_FIRST.md           # Start here
    ├── QUICK_START.md            # 5-minute setup
    ├── SETUP_GUIDE.md            # Detailed guide
    ├── SETUP_CHECKLIST.md        # Step-by-step
    ├── IMPROVEMENT_TASKS.md      # 89 tasks
    ├── IMPLEMENTATION_SUMMARY.md # What we built
    └── ARCHITECTURE.md           # This file
```

---

## 🔌 API Endpoints

### POST /analyze
**Status:** ✅ Implemented  
**Purpose:** Analyze and modernize a repository

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
  "original_code": "...",
  "modernized_code": "...",
  "summary": "✅ Code successfully modernized..."
}
```

**What it does:**
1. Validates URL
2. Creates database record
3. Clones repository
4. Extracts metadata
5. Analyzes code
6. Transforms with AI
7. Saves to database
8. Returns results

### GET /api/repositories
**Status:** ✅ Implemented  
**Purpose:** List all analyzed repositories

**Response:**
```json
{
  "repositories": [
    {
      "id": "uuid",
      "url": "https://github.com/user/repo",
      "name": "repo",
      "status": "complete",
      ...
    }
  ],
  "total": 1
}
```

### GET /api/repositories/:id
**Status:** ✅ Implemented  
**Purpose:** Get repository details

### GET /api/repositories/:id/analysis
**Status:** ✅ Implemented  
**Purpose:** Get analysis results

### GET /health
**Status:** ✅ Implemented  
**Purpose:** Check system health

**Response:**
```json
{
  "status": "healthy",
  "ai_engine": "configured",
  "database": "connected"
}
```

---

## 🔧 Technology Stack

### Backend
- **Framework:** FastAPI 0.104+
- **Database:** Neon Postgres (via SQLAlchemy 2.0+)
- **ORM:** SQLAlchemy with Alembic migrations
- **Git Operations:** GitPython 3.1+
- **AI:** Google Gemini API
- **Testing:** pytest 7.4+, Hypothesis 6.92+
- **Validation:** Pydantic 2.5+

### Frontend
- **Framework:** Next.js 16
- **Language:** TypeScript 5
- **Styling:** Tailwind CSS 4
- **UI Components:** Custom (CodeDiff, Terminal)
- **State:** React 19

### Infrastructure
- **Database:** Neon Postgres (serverless)
- **Storage:** Local filesystem (temp_repos/)
- **Caching:** Redis (planned)
- **Queue:** Celery (planned)

---

## 🚀 Deployment Architecture (Planned)

```
┌─────────────────────────────────────────────────────────────┐
│                         PRODUCTION                          │
│                                                             │
│  ┌──────────────┐         ┌──────────────┐                │
│  │   Vercel     │         │   Railway    │                │
│  │  (Frontend)  │◄───────►│  (Backend)   │                │
│  └──────────────┘         └──────────────┘                │
│                                  │                          │
│                                  ▼                          │
│                           ┌──────────────┐                 │
│                           │     Neon     │                 │
│                           │  (Postgres)  │                 │
│                           └──────────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Current Implementation Status

### ✅ Phase 1: Core Infrastructure (COMPLETE)
- ✅ Database models and connection
- ✅ Repository cloning service
- ✅ GitHub integration (MCP)
- ✅ API endpoints (5 endpoints)
- ✅ Basic analysis flow

### 🔄 Phase 2: Real Analysis (NEXT)
- ⏳ Multi-file scanning
- ⏳ Dependency extraction
- ⏳ Framework detection
- ⏳ Language detection
- ⏳ Analysis storage

### ⏳ Phase 3: Property-Based Testing
- ⏳ Hypothesis setup
- ⏳ Property tests (30 properties)
- ⏳ Test generators

### ⏳ Phase 4: Background Processing
- ⏳ Celery setup
- ⏳ Task queue
- ⏳ Async analysis

### ⏳ Phase 5: Frontend Enhancement
- ⏳ Monaco Editor integration
- ⏳ File tree component
- ⏳ Split view dashboard
- ⏳ Real-time updates

---

## 🔐 Security Considerations

### Current Implementation
- ✅ Environment variables for secrets
- ✅ SSL/TLS for database (Neon)
- ✅ Input validation (URL validation)
- ✅ CORS configuration
- ✅ SQL injection prevention (SQLAlchemy)

### Planned
- ⏳ OAuth authentication
- ⏳ JWT tokens
- ⏳ Rate limiting
- ⏳ API key management
- ⏳ Audit logging

---

## 📈 Scalability Considerations

### Current Limitations
- Synchronous processing (blocking)
- Single server instance
- Local file storage
- No caching layer

### Planned Improvements
- Celery for async processing
- Redis for caching
- S3 for file storage
- Horizontal scaling with Kubernetes
- Load balancing

---

## 🎯 Next Steps

See **IMPROVEMENT_TASKS.md** for detailed roadmap (89 tasks).

**Immediate priorities:**
1. Multi-file analysis (Task 2.2)
2. Analysis storage (Task 2.7)
3. Property-based tests (Tasks 3.1-3.6)
4. Background processing (Tasks 4.1-4.5)
5. Frontend enhancement (Tasks 5.1-5.7)

---

**Last Updated:** December 3, 2024  
**Version:** 1.0.0 (Phase 1 Complete)
