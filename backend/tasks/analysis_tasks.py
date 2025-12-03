"""
Celery tasks for repository analysis.
"""

import logging
from pathlib import Path

from celery_app import celery_app
from database import get_db_context
from models.repository import LegacyRepo, RepoStatus
from services.repository_ingester import get_ingester
from services.analysis_service import get_analysis_service

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name='tasks.analysis_tasks.analyze_repository_task')
def analyze_repository_task(self, repo_id: str, url: str, github_token: str = None):
    """
    Background task to analyze a repository.
    
    Args:
        repo_id: Repository ID
        url: Repository URL
        github_token: Optional GitHub token
    
    Returns:
        Dictionary with analysis results
    """
    logger.info(f"Starting background analysis for repository: {repo_id}")
    
    # Update task state
    self.update_state(state='CLONING', meta={'status': 'Cloning repository...'})
    
    try:
        with get_db_context() as db:
            # Get repository record
            repo = db.query(LegacyRepo).filter(LegacyRepo.id == repo_id).first()
            
            if not repo:
                raise ValueError(f"Repository {repo_id} not found")
            
            # Clone repository
            ingester = get_ingester()
            repo.status = RepoStatus.CLONING
            db.commit()
            
            repo_path = ingester.clone_repository(url, repo_id, github_token)
            
            # Extract metadata
            metadata = ingester.extract_metadata(repo_path)
            repo.storage_path = str(repo_path)
            repo.repo_metadata = metadata
            db.commit()
            
            logger.info(f"Repository cloned to: {repo_path}")
            
            # Update task state
            self.update_state(state='ANALYZING', meta={'status': 'Analyzing code...'})
            
            # Analyze repository
            analysis_service = get_analysis_service()
            analysis = analysis_service.analyze_repository(repo, db)
            
            logger.info(f"Analysis complete for repository: {repo_id}")
            
            return {
                'status': 'complete',
                'repo_id': repo_id,
                'analysis_id': analysis.id,
                'total_files': analysis.total_files,
                'total_issues': len(analysis.issues),
                'grade': analysis.tech_debt.get('grade', 'N/A')
            }
    
    except Exception as e:
        logger.error(f"Error analyzing repository {repo_id}: {e}")
        
        # Update repository status to failed
        try:
            with get_db_context() as db:
                repo = db.query(LegacyRepo).filter(LegacyRepo.id == repo_id).first()
                if repo:
                    repo.status = RepoStatus.FAILED
                    db.commit()
        except:
            pass
        
        raise
