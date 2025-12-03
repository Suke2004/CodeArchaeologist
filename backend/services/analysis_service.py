"""
Analysis service for coordinating repository analysis and storing results.
"""

from pathlib import Path
from typing import Dict, List
import uuid
import logging
from datetime import datetime

from services.file_scanner import get_scanner, FileInfo
from services.dependency_extractor import get_extractor, Dependency
from services.legacy_detector import LegacyDetector
from models.analysis import AnalysisResult
from models.repository import LegacyRepo, RepoStatus

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for analyzing repositories and storing results."""
    
    def __init__(self):
        self.scanner = get_scanner()
        self.extractor = get_extractor()
        self.detector = LegacyDetector()
    
    def analyze_repository(self, repo: LegacyRepo, db_session) -> AnalysisResult:
        """
        Perform complete analysis of repository.
        
        Args:
            repo: LegacyRepo model instance
            db_session: Database session
        
        Returns:
            AnalysisResult model instance
        """
        logger.info(f"Starting analysis of repository: {repo.name}")
        
        repo_path = Path(repo.storage_path)
        
        # Update repository status
        repo.status = RepoStatus.ANALYZING
        db_session.commit()
        
        try:
            # 1. Scan files
            logger.info("Scanning files...")
            files = self.scanner.scan_directory(repo_path)
            file_stats = self.scanner.get_statistics(files)
            
            # 2. Extract dependencies
            logger.info("Extracting dependencies...")
            dependencies = self.extractor.extract_from_repository(repo_path)
            dep_stats = self.extractor.get_statistics(dependencies)
            
            # 3. Analyze code for legacy patterns
            logger.info("Analyzing code for legacy patterns...")
            all_issues = []
            total_lines = 0
            
            # Analyze Python files
            python_files = [f for f in files if f.language == 'python']
            for file_info in python_files[:50]:  # Limit to first 50 files for now
                try:
                    content = file_info.path.read_text(encoding='utf-8', errors='ignore')
                    lines = content.count('\n') + 1
                    total_lines += lines
                    
                    # Detect issues
                    issues = self.detector.detect_python_issues(content)
                    
                    # Add file path to each issue
                    for issue in issues:
                        issue_dict = issue.to_dict()
                        issue_dict['file'] = str(file_info.relative_path)
                        all_issues.append(issue_dict)
                
                except Exception as e:
                    logger.warning(f"Error analyzing file {file_info.path}: {e}")
                    continue
            
            # 4. Calculate technical debt
            logger.info("Calculating technical debt...")
            from services.legacy_detector import Issue, Severity
            
            # Reconstruct Issue objects for tech debt calculation
            issue_objects = []
            for issue_dict in all_issues:
                issue_obj = Issue(
                    severity=Severity[issue_dict['severity']],
                    pattern=issue_dict['pattern'],
                    description=issue_dict['description'],
                    line_number=issue_dict['line_number'],
                    suggestion=issue_dict['suggestion']
                )
                issue_objects.append(issue_obj)
            
            report = self.detector.generate_report(issue_objects)
            tech_debt = self.detector.calculate_tech_debt(issue_objects)
            
            # 5. Detect languages
            languages = self._calculate_language_percentages(file_stats)
            
            # 6. Detect frameworks
            frameworks = self._detect_frameworks(dependencies, files)
            
            # 7. Create analysis result
            analysis_id = str(uuid.uuid4())
            analysis = AnalysisResult(
                id=analysis_id,
                repo_id=repo.id,
                languages=languages,
                frameworks=frameworks,
                issues=all_issues,
                tech_debt=tech_debt,
                total_files=len(files),
                total_lines=total_lines
            )
            
            # Save to database
            db_session.add(analysis)
            
            # Update repository status
            repo.status = RepoStatus.COMPLETE
            db_session.commit()
            
            logger.info(f"Analysis complete! Found {len(all_issues)} issues in {len(files)} files")
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            repo.status = RepoStatus.FAILED
            db_session.commit()
            raise
    
    def _calculate_language_percentages(self, file_stats: Dict) -> List[Dict]:
        """Calculate language percentages from file statistics."""
        by_language = file_stats.get('by_language', {})
        total = sum(by_language.values())
        
        if total == 0:
            return []
        
        languages = []
        for lang, count in by_language.items():
            if lang != 'unknown' and lang != 'config':
                percentage = round((count / total) * 100, 2)
                languages.append({
                    'name': lang,
                    'percentage': percentage,
                    'file_count': count
                })
        
        # Sort by percentage descending
        languages.sort(key=lambda x: x['percentage'], reverse=True)
        return languages
    
    def _detect_frameworks(self, dependencies: List[Dependency], files: List[FileInfo]) -> List[Dict]:
        """Detect frameworks from dependencies and files."""
        frameworks = []
        
        # Python frameworks
        python_frameworks = {
            'django': 'Django',
            'flask': 'Flask',
            'fastapi': 'FastAPI',
            'tornado': 'Tornado',
            'pyramid': 'Pyramid'
        }
        
        # JavaScript frameworks
        js_frameworks = {
            'react': 'React',
            'vue': 'Vue.js',
            'angular': 'Angular',
            'next': 'Next.js',
            'express': 'Express',
            'nestjs': 'NestJS'
        }
        
        # Check dependencies
        for dep in dependencies:
            dep_name_lower = dep.name.lower()
            
            # Check Python frameworks
            for key, name in python_frameworks.items():
                if key in dep_name_lower:
                    frameworks.append({
                        'name': name,
                        'version': dep.version,
                        'confidence': 'high'
                    })
            
            # Check JavaScript frameworks
            for key, name in js_frameworks.items():
                if key in dep_name_lower:
                    frameworks.append({
                        'name': name,
                        'version': dep.version,
                        'confidence': 'high'
                    })
        
        # Check for framework-specific files
        file_names = {f.path.name for f in files}
        
        if 'manage.py' in file_names:
            if not any(f['name'] == 'Django' for f in frameworks):
                frameworks.append({
                    'name': 'Django',
                    'version': None,
                    'confidence': 'medium'
                })
        
        if 'next.config.js' in file_names or 'next.config.ts' in file_names:
            if not any(f['name'] == 'Next.js' for f in frameworks):
                frameworks.append({
                    'name': 'Next.js',
                    'version': None,
                    'confidence': 'medium'
                })
        
        return frameworks


# Singleton instance
_service = None


def get_analysis_service() -> AnalysisService:
    """Get singleton instance of AnalysisService."""
    global _service
    if _service is None:
        _service = AnalysisService()
    return _service
