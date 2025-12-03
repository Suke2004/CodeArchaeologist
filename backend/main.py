from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import os
from typing import Optional
import asyncio

app = FastAPI(title="CodeArchaeologist API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RepoRequest(BaseModel):
    url: str
    target_lang: str


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
    # Simulate processing delay for effect
    await asyncio.sleep(1)
    
    # Check if AI engine is available
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key and api_key != "placeholder":
        # Use real AI engine
        try:
            from services.ai_engine import resurrect
            
            # Mock original code for demo (in production, clone and analyze repo)
            original_code = """# Legacy Python 2 code
print "Hello, World!"

def process_data(data):
    for key, value in data.iteritems():
        print "Key: %s, Value: %s" % (key, value)

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
"""
            
            modernized_code = await resurrect(original_code, request.target_lang)
            
            return AnalysisResponse(
                original_code=original_code,
                modernized_code=modernized_code,
                summary="Code successfully modernized using AI"
            )
        except Exception as e:
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

        return AnalysisResponse(
            original_code=original_code,
            modernized_code=modernized_code,
            summary="Mock data returned (configure GEMINI_API_KEY for real AI processing)"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    api_configured = bool(os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_API_KEY") != "placeholder")
    return {
        "status": "healthy",
        "ai_engine": "configured" if api_configured else "mock_mode"
    }
