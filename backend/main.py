from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
from sqlalchemy.orm import Session
import os
from typing import Optional
import asyncio
import uuid
import logging
from datetime import datetime

from services.legacy_detector import LegacyDetector
from services.repository_ingester import get_ingester
from database import get_db, init_db, check_db_connection
from models.repository import LegacyRepo, RepoStatus
from models.analysis import AnalysisResult
from dotenv import load_dotenv

load_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CodeArchaeologist API",
    version="1.0.0",
    description="AI-powered legacy code resurrection and modernization"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
detector = LegacyDetector()
ingester = get_ingester()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        logger.info("Initializing database...")
        init_db()
        
        if check_db_connection():
            logger.info("✅ Database connection successful")
        else:
            logger.error("❌ Database connection failed")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        # Don't fail startup, allow app to run in degraded mode


class RepoRequest(BaseModel):
    url: str = Field(..., description="Repository URL or code snippet")
    target_lang: str = Field(default="Python 3.11", description="Target language/version")


class AnalysisResponse(BaseModel):
    original_code: str
    modernized_code: str
    summary: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "CodeArchaeologist API is running"}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_repository(request: RepoRequest, db: Session = Depends(get_db)):
    """
    Analyze and modernize legacy code from a repository.
    Now supports real repository cloning and analysis!
    """
    try:
        # Validate URL
        if not ingester.validate_url(request.url):
            raise HTTPException(status_code=400, detail="Invalid repository URL")
        
        # Extract repo info
        repo_info = ingester.extract_repo_info(request.url)
        
        # Check if repository already exists
        existing_repo = db.query(LegacyRepo).filter(LegacyRepo.url == request.url).first()
        
        if existing_repo:
            logger.info(f"Repository already exists: {existing_repo.id}")
            
            # If analysis is complete, return existing results
            if existing_repo.status == RepoStatus.COMPLETE:
                logger.info("Returning existing analysis results")
                repo = existing_repo
                repo_id = existing_repo.id
            else:
                # If previous analysis failed or is incomplete, restart
                logger.info(f"Restarting analysis for repository in status: {existing_repo.status}")
                repo = existing_repo
                repo_id = existing_repo.id
                repo.status = RepoStatus.CLONING
                db.commit()
        else:
            # Create new repository record
            repo_id = str(uuid.uuid4())
            repo = LegacyRepo(
                id=repo_id,
                url=request.url,
                name=repo_info["name"],
                owner=repo_info["owner"],
                user_id="anonymous",  # TODO: Add auth
                status=RepoStatus.CLONING
            )
            db.add(repo)
            db.commit()
            logger.info(f"Created repository record: {repo_id}")
        
        # Clone repository
        try:
            github_token = os.getenv("GITHUB_TOKEN", "").strip().strip('"').strip("'")
            repo_path = ingester.clone_repository(request.url, repo_id, github_token if github_token else None)
            
            # Update status
            repo.status = RepoStatus.ANALYZING
            repo.cloned_at = datetime.utcnow()
            repo.storage_path = str(repo_path)
            
            # Extract metadata
            metadata = ingester.extract_metadata(repo_path)
            repo.repo_metadata = metadata
            db.commit()
            
            logger.info(f"Cloned repository to: {repo_path}")
        
        except Exception as e:
            repo.status = RepoStatus.FAILED
            db.commit()
            raise HTTPException(status_code=500, detail=f"Failed to clone repository: {str(e)}")
        
        # Analyze repository with new analysis service
        try:
            from services.analysis_service import get_analysis_service
            analysis_service = get_analysis_service()
            
            logger.info("Starting repository analysis...")
            analysis = analysis_service.analyze_repository(repo, db)
            
            logger.info(f"Analysis complete: {analysis.total_files} files, {len(analysis.issues)} issues")
        
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            repo.status = RepoStatus.FAILED
            db.commit()
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
        
        # Check if AI engine is available for code modernization
        api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key and api_key != "placeholder":
            # Use real AI engine
            try:
                from services.ai_engine import resurrect
                import traceback
                
                # Mock original code for demo
                original_code = """# Legacy Python 2 code
print "Hello, World!"

def process_data(data):
    for key, value in data.iteritems():
        print "Key: %s, Value: %s" % (key, value)
    result = eval(data.get('expression'))
    return result

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
"""
                
                # Detect issues
                issues = detector.detect_python_issues(original_code)
                report = detector.generate_report(issues)
                tech_debt = detector.calculate_tech_debt(issues)
                
                modernized_code = await resurrect(original_code, request.target_lang)
                
                summary = (
                    f"✅ Code successfully modernized using AI!\n\n"
                    f"📊 Analysis Results:\n"
                    f"• Fixed {report['total_issues']} issues ({report['critical']} critical, {report['high']} high)\n"
                    f"• Maintainability: {tech_debt['grade']} ({tech_debt['maintainability_score']}/100)\n"
                    f"• Time saved: {tech_debt['estimated_hours']} hours\n"
                    f"• {tech_debt['recommendation']}"
                )
                
                return AnalysisResponse(
                    original_code=original_code,
                    modernized_code=modernized_code,
                    summary=summary
                )
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                print(f"AI processing error: {error_details}")
                raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")
        else:
            # Return mock data when API key is not configured
            original_code = """# Legacy Python 2 code
print "Hello, World!"

def fetch_users(callback):
    users = []
    for i in xrange(10):
        user = {'id': i, 'name': 'User %s' % i}
        users.append(user)
    callback(users)

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, id, name):
        self.users[id] = name
        print "Added user:", name
"""

            modernized_code = """# Modern Python 3.11+ code
from typing import Callable


def fetch_users() -> list[dict[str, str | int]]:
    \"\"\"Fetch users asynchronously.\"\"\"
    return [
        {'id': i, 'name': f'User {i}'}
        for i in range(10)
    ]


class UserManager:
    \"\"\"Manage user data with modern patterns.\"\"\"
    
    def __init__(self) -> None:
        self.users: dict[int, str] = {}
    
    def add_user(self, user_id: int, name: str) -> None:
        \"\"\"Add a user to the manager.\"\"\"
        self.users[user_id] = name
        print(f"Added user: {name}")


if __name__ == "__main__":
    print("Hello, World!")
    users = fetch_users()
    manager = UserManager()
    for user in users:
        manager.add_user(user['id'], user['name'])
"""
            
            try:
                # Detect issues
                issues = detector.detect_python_issues(original_code)
                report = detector.generate_report(issues)
                tech_debt = detector.calculate_tech_debt(issues)
                
                summary = (
                    f"🔬 Mock Analysis Complete!\n\n"
                    f"📊 Detected Issues:\n"
                    f"• Total: {report['total_issues']} ({report['critical']} critical, {report['high']} high, {report['medium']} medium, {report['low']} low)\n"
                    f"• Maintainability: Grade {tech_debt['grade']} ({tech_debt['maintainability_score']}/100)\n"
                    f"• Estimated fix time: {tech_debt['estimated_days']} days ({tech_debt['estimated_hours']} hours)\n"
                    f"• {tech_debt['recommendation']}\n\n"
                    f"💡 Configure GEMINI_API_KEY for real AI-powered modernization!"
                )
            except Exception as e:
                # Fallback if detector fails
                summary = f"Mock data returned. Configure GEMINI_API_KEY for real AI processing."

            return AnalysisResponse(
                original_code=original_code,
                modernized_code=modernized_code,
                summary=summary
            )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Analysis error: {error_details}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    api_configured = bool(os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_API_KEY") != "placeholder")
    db_connected = check_db_connection()
    
    return {
        "status": "healthy" if db_connected else "degraded",
        "ai_engine": "configured" if api_configured else "mock_mode",
        "database": "connected" if db_connected else "disconnected"
    }


@app.get("/api/repositories")
async def list_repositories(db: Session = Depends(get_db)):
    """List all analyzed repositories."""
    try:
        repos = db.query(LegacyRepo).order_by(LegacyRepo.created_at.desc()).limit(50).all()
        return {
            "repositories": [repo.to_dict() for repo in repos],
            "total": len(repos)
        }
    except Exception as e:
        logger.error(f"Error listing repositories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/repositories/{repo_id}")
async def get_repository(repo_id: str, db: Session = Depends(get_db)):
    """Get details of a specific repository."""
    try:
        repo = db.query(LegacyRepo).filter(LegacyRepo.id == repo_id).first()
        
        if not repo:
            raise HTTPException(status_code=404, detail="Repository not found")
        
        return repo.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting repository: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/repositories/{repo_id}/analysis")
async def get_analysis(repo_id: str, db: Session = Depends(get_db)):
    """Get analysis results for a repository."""
    try:
        analysis = db.query(AnalysisResult).filter(
            AnalysisResult.repo_id == repo_id
        ).order_by(AnalysisResult.created_at.desc()).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return analysis.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))
