"""
Dependency extraction service for analyzing project dependencies.
Extracts dependencies from various package manager files.
"""

from pathlib import Path
from typing import List, Dict, Optional
import json
import re
import logging

logger = logging.getLogger(__name__)


class Dependency:
    """Represents a project dependency."""
    
    def __init__(
        self,
        name: str,
        version: Optional[str] = None,
        ecosystem: str = 'unknown',
        is_dev: bool = False
    ):
        self.name = name
        self.version = version
        self.ecosystem = ecosystem
        self.is_dev = is_dev
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'version': self.version,
            'ecosystem': self.ecosystem,
            'is_dev': self.is_dev
        }
    
    def __repr__(self):
        return f"<Dependency {self.name}@{self.version} ({self.ecosystem})>"


class DependencyExtractor:
    """Service for extracting dependencies from project files."""
    
    def extract_from_requirements_txt(self, file_path: Path) -> List[Dependency]:
        """
        Extract dependencies from requirements.txt.
        
        Args:
            file_path: Path to requirements.txt
        
        Returns:
            List of Dependency objects
        """
        dependencies = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            for line in content.split('\n'):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Skip -r or -e flags
                if line.startswith('-'):
                    continue
                
                # Parse package name and version
                # Format: package==1.0.0 or package>=1.0.0
                match = re.match(r'^([a-zA-Z0-9\-_\.]+)([><=!]+)?(.+)?', line)
                if match:
                    name = match.group(1)
                    version = match.group(3) if match.group(3) else None
                    
                    dependencies.append(Dependency(
                        name=name,
                        version=version,
                        ecosystem='pip'
                    ))
            
            logger.info(f"Extracted {len(dependencies)} dependencies from requirements.txt")
        
        except Exception as e:
            logger.error(f"Error reading requirements.txt: {e}")
        
        return dependencies
    
    def extract_from_package_json(self, file_path: Path) -> List[Dependency]:
        """
        Extract dependencies from package.json.
        
        Args:
            file_path: Path to package.json
        
        Returns:
            List of Dependency objects
        """
        dependencies = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            data = json.loads(content)
            
            # Extract regular dependencies
            if 'dependencies' in data:
                for name, version in data['dependencies'].items():
                    dependencies.append(Dependency(
                        name=name,
                        version=version,
                        ecosystem='npm',
                        is_dev=False
                    ))
            
            # Extract dev dependencies
            if 'devDependencies' in data:
                for name, version in data['devDependencies'].items():
                    dependencies.append(Dependency(
                        name=name,
                        version=version,
                        ecosystem='npm',
                        is_dev=True
                    ))
            
            logger.info(f"Extracted {len(dependencies)} dependencies from package.json")
        
        except Exception as e:
            logger.error(f"Error reading package.json: {e}")
        
        return dependencies
    
    def extract_from_pyproject_toml(self, file_path: Path) -> List[Dependency]:
        """
        Extract dependencies from pyproject.toml.
        
        Args:
            file_path: Path to pyproject.toml
        
        Returns:
            List of Dependency objects
        """
        dependencies = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Simple parsing for dependencies section
            # Format: package = "^1.0.0" or package = ">=1.0.0"
            in_dependencies = False
            
            for line in content.split('\n'):
                line = line.strip()
                
                # Check if we're in dependencies section
                if line.startswith('[tool.poetry.dependencies]') or line.startswith('[project.dependencies]'):
                    in_dependencies = True
                    continue
                elif line.startswith('[') and in_dependencies:
                    in_dependencies = False
                
                # Parse dependency line
                if in_dependencies and '=' in line:
                    match = re.match(r'^([a-zA-Z0-9\-_]+)\s*=\s*["\']([^"\']+)["\']', line)
                    if match:
                        name = match.group(1)
                        version = match.group(2).lstrip('^~>=<')
                        
                        # Skip python version
                        if name.lower() != 'python':
                            dependencies.append(Dependency(
                                name=name,
                                version=version,
                                ecosystem='pip'
                            ))
            
            logger.info(f"Extracted {len(dependencies)} dependencies from pyproject.toml")
        
        except Exception as e:
            logger.error(f"Error reading pyproject.toml: {e}")
        
        return dependencies
    
    def extract_from_repository(self, repo_path: Path) -> List[Dependency]:
        """
        Extract all dependencies from repository.
        
        Args:
            repo_path: Path to repository root
        
        Returns:
            List of all Dependency objects
        """
        all_dependencies = []
        
        # Check for requirements.txt
        requirements_file = repo_path / 'requirements.txt'
        if requirements_file.exists():
            all_dependencies.extend(self.extract_from_requirements_txt(requirements_file))
        
        # Check for package.json
        package_json = repo_path / 'package.json'
        if package_json.exists():
            all_dependencies.extend(self.extract_from_package_json(package_json))
        
        # Check for pyproject.toml
        pyproject_toml = repo_path / 'pyproject.toml'
        if pyproject_toml.exists():
            all_dependencies.extend(self.extract_from_pyproject_toml(pyproject_toml))
        
        logger.info(f"Total dependencies extracted: {len(all_dependencies)}")
        return all_dependencies
    
    def get_statistics(self, dependencies: List[Dependency]) -> Dict:
        """
        Get statistics about dependencies.
        
        Args:
            dependencies: List of Dependency objects
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total': len(dependencies),
            'by_ecosystem': {},
            'dev_dependencies': 0,
            'prod_dependencies': 0
        }
        
        for dep in dependencies:
            # Count by ecosystem
            stats['by_ecosystem'][dep.ecosystem] = stats['by_ecosystem'].get(dep.ecosystem, 0) + 1
            
            # Count dev vs prod
            if dep.is_dev:
                stats['dev_dependencies'] += 1
            else:
                stats['prod_dependencies'] += 1
        
        return stats


# Singleton instance
_extractor = None


def get_extractor() -> DependencyExtractor:
    """Get singleton instance of DependencyExtractor."""
    global _extractor
    if _extractor is None:
        _extractor = DependencyExtractor()
    return _extractor
