"""
File scanner service for analyzing repository contents.
Scans directories and identifies files for analysis.
"""

from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# File extensions to analyze
PYTHON_EXTENSIONS = {'.py', '.pyw'}
JAVASCRIPT_EXTENSIONS = {'.js', '.jsx', '.mjs', '.cjs'}
TYPESCRIPT_EXTENSIONS = {'.ts', '.tsx'}
CONFIG_FILES = {
    'requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile',
    'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'
}

# Directories to ignore
IGNORE_DIRS = {
    '.git', '.svn', '.hg',
    'node_modules', '__pycache__', '.pytest_cache',
    'venv', 'env', '.venv', '.env',
    'dist', 'build', '.next', '.nuxt',
    'coverage', '.coverage', 'htmlcov',
    '.idea', '.vscode', '.vs',
    'target', 'bin', 'obj'
}


class FileInfo:
    """Information about a scanned file."""
    
    def __init__(self, path: Path, relative_path: Path, size: int, extension: str):
        self.path = path
        self.relative_path = relative_path
        self.size = size
        self.extension = extension
        self.language = self._detect_language()
    
    def _detect_language(self) -> str:
        """Detect programming language from extension."""
        if self.extension in PYTHON_EXTENSIONS:
            return 'python'
        elif self.extension in JAVASCRIPT_EXTENSIONS:
            return 'javascript'
        elif self.extension in TYPESCRIPT_EXTENSIONS:
            return 'typescript'
        elif self.path.name in CONFIG_FILES:
            return 'config'
        else:
            return 'unknown'
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'path': str(self.relative_path),
            'size': self.size,
            'extension': self.extension,
            'language': self.language
        }


class FileScanner:
    """Service for scanning repository files."""
    
    def __init__(self, ignore_dirs: Optional[set] = None):
        """
        Initialize file scanner.
        
        Args:
            ignore_dirs: Additional directories to ignore
        """
        self.ignore_dirs = IGNORE_DIRS.copy()
        if ignore_dirs:
            self.ignore_dirs.update(ignore_dirs)
    
    def should_ignore_dir(self, dir_path: Path) -> bool:
        """
        Check if directory should be ignored.
        
        Args:
            dir_path: Directory path to check
        
        Returns:
            True if directory should be ignored
        """
        return dir_path.name in self.ignore_dirs
    
    def should_analyze_file(self, file_path: Path) -> bool:
        """
        Check if file should be analyzed.
        
        Args:
            file_path: File path to check
        
        Returns:
            True if file should be analyzed
        """
        # Check if it's a config file
        if file_path.name in CONFIG_FILES:
            return True
        
        # Check extension
        ext = file_path.suffix.lower()
        return ext in (PYTHON_EXTENSIONS | JAVASCRIPT_EXTENSIONS | TYPESCRIPT_EXTENSIONS)
    
    def scan_directory(self, repo_path: Path, max_files: int = 1000) -> List[FileInfo]:
        """
        Scan directory and return list of files to analyze.
        
        Args:
            repo_path: Path to repository root
            max_files: Maximum number of files to scan
        
        Returns:
            List of FileInfo objects
        """
        files = []
        file_count = 0
        
        try:
            for item in repo_path.rglob('*'):
                # Stop if we've scanned too many files
                if file_count >= max_files:
                    logger.warning(f"Reached max file limit ({max_files}), stopping scan")
                    break
                
                # Skip if in ignored directory
                if any(self.should_ignore_dir(parent) for parent in item.parents):
                    continue
                
                # Only process files
                if not item.is_file():
                    continue
                
                file_count += 1
                
                # Check if we should analyze this file
                if self.should_analyze_file(item):
                    try:
                        size = item.stat().st_size
                        relative_path = item.relative_to(repo_path)
                        
                        file_info = FileInfo(
                            path=item,
                            relative_path=relative_path,
                            size=size,
                            extension=item.suffix.lower()
                        )
                        files.append(file_info)
                    
                    except Exception as e:
                        logger.warning(f"Error processing file {item}: {e}")
                        continue
            
            logger.info(f"Scanned {file_count} files, found {len(files)} files to analyze")
            return files
        
        except Exception as e:
            logger.error(f"Error scanning directory: {e}")
            return []
    
    def get_statistics(self, files: List[FileInfo]) -> Dict:
        """
        Get statistics about scanned files.
        
        Args:
            files: List of FileInfo objects
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_files': len(files),
            'total_size': sum(f.size for f in files),
            'by_language': {},
            'by_extension': {}
        }
        
        # Count by language
        for file in files:
            lang = file.language
            stats['by_language'][lang] = stats['by_language'].get(lang, 0) + 1
        
        # Count by extension
        for file in files:
            ext = file.extension
            stats['by_extension'][ext] = stats['by_extension'].get(ext, 0) + 1
        
        return stats


# Singleton instance
_scanner = None


def get_scanner() -> FileScanner:
    """Get singleton instance of FileScanner."""
    global _scanner
    if _scanner is None:
        _scanner = FileScanner()
    return _scanner
