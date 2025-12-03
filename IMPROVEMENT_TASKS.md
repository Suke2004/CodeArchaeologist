# CodeArchaeologist - Improvement Tasks

**Status:** Ready for Implementation  
**Last Updated:** December 3, 2024  
**Priority:** High → Low (top to bottom within each phase)

---

## 📋 Task Overview

This document contains all tasks needed to bring CodeArchaeologist from its current MVP state (30% complete) to a fully functional application matching the original spec.

**Current State:**
- ✅ Basic API with mock data
- ✅ AI integration (Gemini)
- ✅ Legacy pattern detector
- ✅ Unit tests
- ❌ No database
- ❌ No real repository analysis
- ❌ No property-based tests
- ❌ No task queue

**Target State:**
- Full repository analysis
- Database persistence
- Real GitHub integration
- Property-based testing
- Background task processing
- Complete frontend integration

---

## 🚀 Phase 1: Core Infrastructure (CRITICAL)

### Database & Persistence

- [ ] **1.1 Set up PostgreSQL database**
  - Install PostgreSQL locally or use Docker
  - Create database: `codearchaeologist_dev`
  - Configure connection string in `.env`
  - Test connection
  - _Priority: CRITICAL_
  - _Estimated Time: 1 hour_

- [ ] **1.2 Install SQLAlchemy and dependencies**
  - Add to `requirements.txt`: `sqlalchemy>=2.0.0`, `psycopg2-binary>=2.9.0`, `alembic>=1.12.0`
  - Install: `pip install -r requirements.txt`
  - _Priority: CRITICAL_
  - _Estimated Time: 15 minutes_

- [ ] **1.3 Create SQLAlchemy models**
  - Create `backend/models/__init__.py`
  - Create `backend/models/repository.py` with `LegacyRepo` model
  - Create `backend/models/analysis.py` with `AnalysisResult` model
  - Create `backend/models/migration_plan.py` with `MigrationPlan` model
  - Add relationships between models
  - _Priority: CRITICAL_
  - _Estimated Time: 2 hours_
  - _References: Design doc data models section_

- [ ] **1.4 Set up Alembic migrations**
  - Initialize Alembic: `alembic init alembic`
  - Configure `alembic.ini` with database URL
  - Create initial migration: `alembic revision --autogenerate -m "Initial schema"`
  - Run migration: `alembic upgrade head`
  - _Priority: CRITICAL_
  - _Estimated Time: 1 hour_

- [ ] **1.5 Create database session management**
  - Create `backend/database.py` with session factory
  - Add dependency injection for FastAPI routes
  - Implement connection pooling
  - Add health check for database
  - _Priority: CRITICAL_
  - _Estimated Time: 1 hour_

- [ ] **1.6 Install and configure Redis**
  - Install Redis locally or use Docker
  - Add to `requirements.txt`: `redis>=5.0.0`, `aioredis>=2.0.0`
  - Create `backend/cache.py` with Redis client
  - Test connection
  - _Priority: HIGH_
  - _Estimated Time: 30 minutes_

### Repository Integration

- [ ] **1.7 Install GitPython**
  - Add to `requirements.txt`: `GitPython>=3.1.40`
  - Install: `pip install GitPython`
  - _Priority: CRITICAL_
  - _Estimated Time: 5 minutes_

- [ ] **1.8 Create Repository Ingester service**
  - Create `backend/services/repository_ingester.py`
  - Implement `validate_url(url: str) -> bool`
  - Implement `clone_repository(url: str, dest: str) -> Path`
  - Implement `extract_metadata(repo_path: Path) -> dict`
  - Add error handling for invalid URLs, network issues
  - _Priority: CRITICAL_
  - _Estimated Time: 3 hours_
  - _References: Requirements 1.1, 1.2, 1.3, 1.4_

- [ ] **1.9 Integrate MCP GitHub connector**
  - Move MCP connector to backend services
  - Create `backend/services/github_service.py` wrapper
  - Implement `clone_with_mcp(url: str) -> dict`
  - Implement `get_repo_metadata(url: str) -> dict`
  - Test with real GitHub repository
  - _Priority: HIGH_
  - _Estimated Time: 2 hours_

- [ ] **1.10 Update /analyze endpoint to use real repos**
  - Remove hardcoded mock data
  - Accept repository URL
  - Clone repository using ingester
  - Store in temporary directory
  - Return cloned path
  - _Priority: CRITICAL_
  - _Estimated Time: 1 hour_

---

## 🔍 Phase 2: Real Analysis Engine (HIGH PRIORITY)

### Multi-File Analysis

- [ ] **2.1 Create file scanner**
  - Create `backend/services/file_scanner.py`
  - Implement `scan_directory(path: Path) -> List[FileInfo]`
  - Filter by file extensions (.py, .js, .ts, etc.)
  - Ignore common directories (node_modules, .git, venv)
  - Return file paths with metadata
  - _Priority: HIGH_
  - _Estimated Time: 2 hours_

- [ ] **2.2 Extend legacy detector for multi-file**
  - Update `LegacyDetector.detect_python_issues()` to accept file path
  - Create `analyze_file(file_path: Path) -> List[Issue]`
  - Create `analyze_repository(repo_path: Path) -> Dict[str, List[Issue]]`
  - Aggregate issues across all files
  - _Priority: HIGH_
  - _Estimated Time: 2 hours_

- [ ] **2.3 Implement language detection**
  - Install `pygments` or use file extensions
  - Create `backend/services/language_detector.py`
  - Implement `detect_languages(repo_path: Path) -> List[LanguageInfo]`
  - Calculate percentages by line count
  - _Priority: MEDIUM_
  - _Estimated Time: 2 hours_
  - _References: Requirements 2.1_

- [ ] **2.4 Implement dependency extraction**
  - Create `backend/services/dependency_extractor.py`
  - Implement `extract_python_deps(repo_path: Path) -> List[Dependency]`
    - Parse requirements.txt
    - Parse pyproject.toml
    - Parse setup.py
  - Implement `extract_js_deps(repo_path: Path) -> List[Dependency]`
    - Parse package.json
  - Return structured dependency list
  - _Priority: HIGH_
  - _Estimated Time: 3 hours_
  - _References: Requirements 2.2_

- [ ] **2.5 Build dependency graph**
  - Create `backend/services/dependency_graph.py`
  - Implement `build_graph(dependencies: List[Dependency]) -> DependencyGraph`
  - Identify direct vs transitive dependencies
  - Check for outdated versions (use PyPI/npm APIs)
  - Check for security vulnerabilities
  - _Priority: MEDIUM_
  - _Estimated Time: 4 hours_
  - _References: Requirements 2.3_

- [ ] **2.6 Implement framework detection**
  - Create `backend/services/framework_detector.py`
  - Detect Django (settings.py, manage.py)
  - Detect Flask (app.py with Flask import)
  - Detect FastAPI (main.py with FastAPI import)
  - Detect React (package.json with react)
  - Detect Next.js (next.config.js)
  - Return framework name and version
  - _Priority: MEDIUM_
  - _Estimated Time: 2 hours_
  - _References: Requirements 2.4_

### Analysis Storage

- [ ] **2.7 Create analysis service**
  - Create `backend/services/analysis_service.py`
  - Implement `save_analysis(repo_id: str, analysis: AnalysisResult) -> None`
  - Implement `get_analysis(repo_id: str) -> AnalysisResult`
  - Use SQLAlchemy models
  - _Priority: HIGH_
  - _Estimated Time: 2 hours_

- [ ] **2.8 Update API endpoints for persistence**
  - Modify POST `/analyze` to save to database
  - Create GET `/api/repositories/:id/analysis`
  - Create GET `/api/repositories` (list all)
  - Return stored analysis results
  - _Priority: HIGH_
  - _Estimated Time: 2 hours_
  - _References: Requirements 8.1, 8.2, 8.3_

---

## 🧪 Phase 3: Property-Based Testing (MEDIUM PRIORITY)

### Setup Property Testing

- [ ] **3.1 Install Hypothesis**
  - Add to `requirements.txt`: `hypothesis>=6.92.0`
  - Install: `pip install hypothesis`
  - _Priority: MEDIUM_
  - _Estimated Time: 5 minutes_

- [ ] **3.2 Create test generators**
  - Create `backend/tests/generators.py`
  - Implement `generate_git_url() -> str`
  - Implement `generate_python_code() -> str`
  - Implement `generate_repository() -> LegacyRepo`
  - Implement `generate_analysis_result() -> AnalysisResult`
  - _Priority: MEDIUM_
  - _Estimated Time: 3 hours_

- [ ] **3.3 Write property test for URL validation**
  - Create `backend/tests/test_properties_ingestion.py`
  - **Property 2: Invalid input rejection**
  - Test: For any invalid URL, system rejects with error
  - Tag: `# Feature: code-archaeologist, Property 2: Invalid input rejection`
  - _Priority: MEDIUM_
  - _Estimated Time: 1 hour_
  - _Validates: Requirements 1.2_

- [ ] **3.4 Write property test for repository ingestion**
  - Add to `backend/tests/test_properties_ingestion.py`
  - **Property 1: Repository ingestion completeness**
  - Test: For any valid URL, clone succeeds and metadata is retrievable
  - Tag: `# Feature: code-archaeologist, Property 1: Repository ingestion completeness`
  - _Priority: MEDIUM_
  - _Estimated Time: 1 hour_
  - _Validates: Requirements 1.1, 1.3, 1.4_

- [ ] **3.5 Write property test for analysis completeness**
  - Create `backend/tests/test_properties_analysis.py`
  - **Property 3: Analysis completeness**
  - Test: For any repository, language percentages sum to 100%
  - Tag: `# Feature: code-archaeologist, Property 3: Analysis completeness`
  - _Priority: MEDIUM_
  - _Estimated Time: 1 hour_
  - _Validates: Requirements 2.1, 2.2, 2.3_

- [ ] **3.6 Write property test for data persistence**
  - Create `backend/tests/test_properties_persistence.py`
  - **Property 20: Data persistence round-trip**
  - Test: For any analysis, store then retrieve returns same data
  - Tag: `# Feature: code-archaeologist, Property 20: Data persistence round-trip`
  - _Priority: MEDIUM_
  - _Estimated Time: 1 hour_
  - _Validates: Requirements 8.1, 8.2, 8.4_

- [ ] **3.7 Configure Hypothesis settings**
  - Update `pytest.ini` with Hypothesis settings
  - Set min iterations: 100
  - Enable shrinking
  - Configure timeout
  - _Priority: LOW_
  - _Estimated Time: 15 minutes_

---

## ⚙️ Phase 4: Background Processing (MEDIUM PRIORITY)

### Task Queue Setup

- [ ] **4.1 Install Celery and dependencies**
  - Add to `requirements.txt`: `celery>=5.3.0`, `celery[redis]>=5.3.0`
  - Install: `pip install celery[redis]`
  - _Priority: MEDIUM_
  - _Estimated Time: 10 minutes_

- [ ] **4.2 Configure Celery**
  - Create `backend/celery_app.py`
  - Configure Redis as broker and backend
  - Set up task routes
  - Configure worker settings
  - _Priority: MEDIUM_
  - _Estimated Time: 1 hour_

- [ ] **4.3 Create analysis task**
  - Create `backend/tasks/analysis_tasks.py`
  - Implement `@celery_task analyze_repository_task(repo_url: str, user_id: str)`
  - Clone repository
  - Run analysis
  - Save to database
  - Return task ID
  - _Priority: MEDIUM_
  - _Estimated Time: 2 hours_
  - _References: Requirements 9.1_

- [ ] **4.4 Update API to use tasks**
  - Modify POST `/analyze` to queue Celery task
  - Return task ID immediately
  - Create GET `/api/tasks/:id/status` endpoint
  - Return task progress and result
  - _Priority: MEDIUM_
  - _Estimated Time: 1 hour_

- [ ] **4.5 Implement queue management**
  - Create `backend/services/queue_service.py`
  - Implement `get_queue_position(task_id: str) -> int`
  - Implement `get_estimated_wait_time(task_id: str) -> int`
  - Implement `cancel_task(task_id: str) -> bool`
  - _Priority: LOW_
  - _Estimated Time: 2 hours_
  - _References: Requirements 9.2, 9.5_

---

## 🎨 Phase 5: Frontend Integration (MEDIUM PRIORITY)

### API Integration

- [ ] **5.1 Update frontend API client**
  - Update `frontend/lib/api.ts` (create if missing)
  - Add proper TypeScript types for API responses
  - Handle task-based async flow
  - Add error handling
  - _Priority: MEDIUM_
  - _Estimated Time: 2 hours_

- [ ] **5.2 Implement polling for task status**
  - Create `frontend/hooks/useTaskStatus.ts`
  - Poll `/api/tasks/:id/status` every 2 seconds
  - Update UI with progress
  - Handle completion and errors
  - _Priority: MEDIUM_
  - _Estimated Time: 2 hours_

- [ ] **5.3 Update main page for real data**
  - Modify `frontend/app/page.tsx`
  - Remove mock terminal logs
  - Use real API responses
  - Display actual analysis results
  - _Priority: MEDIUM_
  - _Estimated Time: 2 hours_

### Split View Dashboard

- [ ] **5.4 Install Monaco Editor**
  - Add to `package.json`: `@monaco-editor/react`
  - Install: `npm install @monaco-editor/react`
  - _Priority: MEDIUM_
  - _Estimated Time: 5 minutes_

- [ ] **5.5 Create file tree component**
  - Create `frontend/components/FileTree.tsx`
  - Display hierarchical file structure
  - Show change indicators
  - Handle file selection
  - _Priority: MEDIUM_
  - _Estimated Time: 3 hours_

- [ ] **5.6 Enhance CodeDiff component**
  - Update `frontend/components/CodeDiff.tsx`
  - Integrate Monaco Editor
  - Implement synchronized scrolling
  - Add line-by-line diff highlighting
  - _Priority: MEDIUM_
  - _Estimated Time: 4 hours_
  - _References: Requirements 5.2, 5.3_

- [ ] **5.7 Create split view page**
  - Create `frontend/app/analysis/[id]/page.tsx`
  - Layout: file tree + dual Monaco editors
  - Load files from API
  - Handle file switching
  - _Priority: MEDIUM_
  - _Estimated Time: 3 hours_
  - _References: Requirements 5.1, 5.4, 5.5_

---

## 🤖 Phase 6: AI Enhancements (LOW PRIORITY)

### Migration Strategy

- [ ] **6.1 Create migration strategy generator**
  - Create `backend/services/migration_strategy.py`
  - Implement `generate_strategy(analysis: AnalysisResult) -> MigrationPlan`
  - Use Gemini to analyze dependencies
  - Generate prioritized steps
  - Identify breaking changes
  - _Priority: LOW_
  - _Estimated Time: 4 hours_
  - _References: Requirements 3.1, 3.2_

- [ ] **6.2 Implement refactoring agent**
  - Create `backend/services/refactoring_agent.py`
  - Implement `refactor_file(file_path: Path, plan: MigrationPlan) -> str`
  - Use Gemini for code transformation
  - Apply transformations per file
  - Generate diffs
  - _Priority: LOW_
  - _Estimated Time: 4 hours_
  - _References: Requirements 4.1, 4.3_

- [ ] **6.3 Add API endpoints for migration**
  - Create GET `/api/repositories/:id/plan`
  - Create POST `/api/repositories/:id/refactor`
  - Create GET `/api/repositories/:id/diff`
  - _Priority: LOW_
  - _Estimated Time: 1 hour_

---

## 🔐 Phase 7: Authentication & Security (LOW PRIORITY)

### OAuth Integration

- [ ] **7.1 Install OAuth libraries**
  - Add to `requirements.txt`: `authlib>=1.2.0`, `python-jose>=3.3.0`
  - Install dependencies
  - _Priority: LOW_
  - _Estimated Time: 10 minutes_

- [ ] **7.2 Implement GitHub OAuth**
  - Create `backend/auth/oauth.py`
  - Configure OAuth flow
  - Store tokens securely
  - Add middleware for protected routes
  - _Priority: LOW_
  - _Estimated Time: 4 hours_
  - _References: Requirements 1.1_

- [ ] **7.3 Add JWT authentication**
  - Create `backend/auth/jwt.py`
  - Generate and validate tokens
  - Add authentication middleware
  - Protect API endpoints
  - _Priority: LOW_
  - _Estimated Time: 3 hours_

---

## 📊 Phase 8: Monitoring & Optimization (LOW PRIORITY)

### Caching

- [ ] **8.1 Implement Redis caching**
  - Create `backend/services/cache_service.py`
  - Cache analysis results (24h TTL)
  - Cache dependency graphs (24h TTL)
  - Cache repository metadata (7d TTL)
  - _Priority: LOW_
  - _Estimated Time: 2 hours_

### Logging & Monitoring

- [ ] **8.2 Set up structured logging**
  - Configure Python logging
  - Log all API requests
  - Log analysis stages
  - Log errors with context
  - _Priority: LOW_
  - _Estimated Time: 2 hours_

- [ ] **8.3 Add metrics collection**
  - Track analysis duration
  - Track AI token usage
  - Track queue lengths
  - Export metrics endpoint
  - _Priority: LOW_
  - _Estimated Time: 2 hours_

---

## 🚢 Phase 9: Deployment (LOW PRIORITY)

### Docker Configuration

- [ ] **9.1 Create Dockerfile for backend**
  - Create `backend/Dockerfile`
  - Multi-stage build
  - Optimize image size
  - _Priority: LOW_
  - _Estimated Time: 1 hour_

- [ ] **9.2 Create Docker Compose**
  - Create `docker-compose.yml`
  - Services: backend, frontend, postgres, redis, celery
  - Configure networking
  - Add volume mounts
  - _Priority: LOW_
  - _Estimated Time: 2 hours_

- [ ] **9.3 Create deployment scripts**
  - Create `deploy.sh`
  - Environment setup
  - Database migrations
  - Service startup
  - _Priority: LOW_
  - _Estimated Time: 1 hour_

---

## 🧹 Phase 10: Bug Fixes & Polish (ONGOING)

### Known Issues

- [ ] **10.1 Fix AI model fallback logic**
  - Current code tries multiple model names
  - Simplify to use one working model
  - Add better error messages
  - _Priority: HIGH_
  - _Estimated Time: 30 minutes_

- [ ] **10.2 Improve error handling in analyze endpoint**
  - Add specific error types
  - Return structured error responses
  - Log errors properly
  - _Priority: MEDIUM_
  - _Estimated Time: 1 hour_

- [ ] **10.3 Add input validation**
  - Validate repository URLs properly
  - Check file size limits
  - Validate API request payloads
  - _Priority: MEDIUM_
  - _Estimated Time: 1 hour_

- [ ] **10.4 Update frontend error display**
  - Show user-friendly error messages
  - Add retry buttons
  - Handle network errors
  - _Priority: MEDIUM_
  - _Estimated Time: 1 hour_

- [ ] **10.5 Add loading states**
  - Show spinners during API calls
  - Disable buttons during processing
  - Add skeleton loaders
  - _Priority: LOW_
  - _Estimated Time: 1 hour_

---

## 📝 Testing Tasks (ONGOING)

### Test Coverage

- [ ] **11.1 Increase unit test coverage**
  - Target: 80% coverage
  - Add tests for new services
  - Test error paths
  - _Priority: MEDIUM_
  - _Estimated Time: 4 hours_

- [ ] **11.2 Add integration tests**
  - Test full analysis pipeline
  - Test database operations
  - Test API endpoints end-to-end
  - _Priority: MEDIUM_
  - _Estimated Time: 4 hours_

- [ ] **11.3 Add frontend tests**
  - Install Vitest and Testing Library
  - Test components
  - Test hooks
  - Test API integration
  - _Priority: LOW_
  - _Estimated Time: 4 hours_

---

## 📚 Documentation Tasks (ONGOING)

### Code Documentation

- [ ] **12.1 Add docstrings to all functions**
  - Follow Google style
  - Include examples
  - Document parameters and returns
  - _Priority: LOW_
  - _Estimated Time: 3 hours_

- [ ] **12.2 Update API documentation**
  - Update FastAPI docstrings
  - Add request/response examples
  - Document error codes
  - _Priority: LOW_
  - _Estimated Time: 2 hours_

- [ ] **12.3 Create architecture diagram**
  - Update design doc with actual architecture
  - Create Mermaid diagrams
  - Document data flow
  - _Priority: LOW_
  - _Estimated Time: 2 hours_

---

## 🎯 Quick Wins (Do These First!)

These tasks will give you the biggest impact with least effort:

1. **Task 1.8** - Create Repository Ingester (enables real repo analysis)
2. **Task 1.10** - Update /analyze endpoint (connects everything)
3. **Task 2.2** - Extend legacy detector for multi-file (core feature)
4. **Task 10.1** - Fix AI model fallback (fixes current bugs)
5. **Task 5.3** - Update main page for real data (visible improvement)

---

## 📊 Progress Tracking

**Total Tasks:** 89  
**Completed:** 0  
**In Progress:** 0  
**Blocked:** 0  

**By Phase:**
- Phase 1 (Core Infrastructure): 0/10
- Phase 2 (Real Analysis): 0/8
- Phase 3 (Property Testing): 0/7
- Phase 4 (Background Processing): 0/5
- Phase 5 (Frontend Integration): 0/7
- Phase 6 (AI Enhancements): 0/3
- Phase 7 (Authentication): 0/3
- Phase 8 (Monitoring): 0/3
- Phase 9 (Deployment): 0/3
- Phase 10 (Bug Fixes): 0/5
- Phase 11 (Testing): 0/3
- Phase 12 (Documentation): 0/3

---

## 🎓 How to Use This Document

1. **Start with Phase 1** - Core infrastructure is required for everything else
2. **Check dependencies** - Some tasks require others to be completed first
3. **Update progress** - Mark tasks as complete with ✅
4. **Track time** - Note actual time vs estimated
5. **Add notes** - Document issues or decisions made

**Recommended Daily Goal:** Complete 3-5 tasks per day

**Estimated Total Time:** 120-150 hours (3-4 weeks full-time)

---

## 🆘 Need Help?

- Check the original spec: `.kiro/specs/code-archaeologist/`
- Review steering rules: `.kiro/steering/`
- Run tests: `cd backend && pytest`
- Check API docs: http://localhost:8000/docs

---

**Last Updated:** December 3, 2024  
**Next Review:** After Phase 1 completion
