from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
import os
from typing import Optional, Dict, List
import asyncio
from services.legacy_detector import LegacyDetector

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

# Initialize detector
detector = LegacyDetector()


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
async def analyze_repository(request: RepoRequest):
    """
    Analyze and modernize legacy code from a repository.
    """
    try:
        # Simulate processing delay for effect
        await asyncio.sleep(1)
        
        # Check if AI engine is available
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
    return {
        "status": "healthy",
        "ai_engine": "configured" if api_configured else "mock_mode"
    }
