"""
Repository ingester service for cloning and validating repositories.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime
import logging

import git
from git import Repo, GitCommandError

logger = logging.getLogger(__name__)

# Directory for storing cloned repositories
TEMP_REPOS_DIR = Path(__file__).parent.parent / "temp_repos"
TEMP_REPOS_DIR.mkdir(exist_ok=True)


class RepositoryIngester:
    """Service for cloning and managing repositories."""
    
    # Regex patterns for validating Git URLs
    GIT_URL_PATTERNS = [
        r"^https?://github\.com/[\w\-]+/[\w\-\.]+/?$",
        r"^https?://gitlab\.com/[\w\-]+/[\w\-\.]+/?$",
        r"^https?://bitbucket\.org/[\w\-]+/[\w\-\.]+/?$",
        r"^git@github\.com:[\w\-]+/[\w\-\.]+\.git$",
        r"^git@gitlab\.com:[\w\-]+/[\w\-\.]+\.git$",
    ]
    
    def __init__(self, storage_dir: Optional[Path] = None):
        """
        Initialize repository ingester.
        
        Args:
            storage_dir: Directory to store cloned repositories (default: temp_repos/)
        """
        self.storage_dir = storage_dir or TEMP_REPOS_DIR
        self.storage_dir.mkdir(exist_ok=True)
    
    def validate_url(self, url: str) -> bool:
        """
        Validate if URL is a valid Git repository URL.
        
        Args:
            url: Repository URL to validate
        
        Returns:
            True if valid, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        
        # Remove trailing slashes and .git
        url = url.rstrip("/").rstrip(".git")
        
        # Check against patterns
        for pattern in self.GIT_URL_PATTERNS:
            if re.match(pattern, url) or re.match(pattern, url + ".git"):
                return True
        
        return False
    
    def extract_repo_info(self, url: str) -> Dict[str, str]:
        """
        Extract repository name and owner from URL.
        
        Args:
            url: Repository URL
        
        Returns:
            Dictionary with 'owner' and 'name' keys
        """
        # Remove protocol and trailing slashes
        clean_url = url.replace("https://", "").replace("http://", "")
        clean_url = clean_url.replace("git@", "").replace(":", "/")
        clean_url = clean_url.rstrip("/").rstrip(".git")
        
        # Split path
        parts = clean_url.split("/")
        
        if len(parts) >= 3:
            owner = parts[-2]
            name = parts[-1]
            return {"owner": owner, "name": name}
        
        return {"owner": "unknown", "name": "unknown"}
    
    def clone_repository(
        self, 
        url: str, 
        repo_id: str,
        github_token: Optional[str] = None
    ) -> Path:
        """
        Clone a repository to local storage.
        
        Args:
            url: Repository URL to clone
            repo_id: Unique identifier for this repository
            github_token: Optional GitHub token for private repos
        
        Returns:
            Path to cloned repository
        
        Raises:
            ValueError: If URL is invalid
            GitCommandError: If cloning fails
        """
        if not self.validate_url(url):
            raise ValueError(f"Invalid repository URL: {url}")
        
        # Create destination path
        repo_info = self.extract_repo_info(url)
        dest_path = self.storage_dir / f"{repo_id}_{repo_info['name']}"
        
        # Remove if already exists
        if dest_path.exists():
            logger.warning(f"Repository already exists at {dest_path}, removing...")
            shutil.rmtree(dest_path)
        
        # Add token to URL if provided
        clone_url = url
        if github_token and "github.com" in url:
            clone_url = url.replace("https://", f"https://{github_token}@")
        
        try:
            logger.info(f"Cloning repository from {url} to {dest_path}")
            Repo.clone_from(clone_url, dest_path, depth=1)  # Shallow clone for speed
            logger.info(f"Successfully cloned repository to {dest_path}")
            return dest_path
        
        except GitCommandError as e:
            logger.error(f"Failed to clone repository: {e}")
            # Clean up partial clone
            if dest_path.exists():
                shutil.rmtree(dest_path)
            raise
    
    def extract_metadata(self, repo_path: Path) -> Dict:
        """
        Extract metadata from cloned repository.
        
        Args:
            repo_path: Path to cloned repository
        
        Returns:
            Dictionary with repository metadata
        """
        try:
            repo = Repo(repo_path)
            
            # Get default branch
            try:
                default_branch = repo.active_branch.name
            except:
                default_branch = "main"
            
            # Get last commit info
            try:
                last_commit = repo.head.commit
                last_commit_date = datetime.fromtimestamp(last_commit.committed_date)
                last_commit_message = last_commit.message.strip()
            except:
                last_commit_date = None
                last_commit_message = None
            
            # Count files
            file_count = sum(1 for _ in repo_path.rglob("*") if _.is_file())
            
            # Calculate size (in MB)
            size_bytes = sum(f.stat().st_size for f in repo_path.rglob("*") if f.is_file())
            size_mb = round(size_bytes / (1024 * 1024), 2)
            
            return {
                "default_branch": default_branch,
                "last_commit_date": last_commit_date.isoformat() if last_commit_date else None,
                "last_commit_message": last_commit_message,
                "file_count": file_count,
                "size_mb": size_mb,
            }
        
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {
                "default_branch": "unknown",
                "last_commit_date": None,
                "last_commit_message": None,
                "file_count": 0,
                "size_mb": 0,
            }
    
    def cleanup_repository(self, repo_path: Path) -> bool:
        """
        Remove cloned repository from storage.
        
        Args:
            repo_path: Path to repository to remove
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if repo_path.exists():
                shutil.rmtree(repo_path)
                logger.info(f"Cleaned up repository at {repo_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error cleaning up repository: {e}")
            return False


# Singleton instance
_ingester = None


def get_ingester() -> RepositoryIngester:
    """Get singleton instance of RepositoryIngester."""
    global _ingester
    if _ingester is None:
        _ingester = RepositoryIngester()
    return _ingester
