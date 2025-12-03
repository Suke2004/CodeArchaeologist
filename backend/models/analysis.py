"""
Analysis result model for storing code analysis data.
"""

from sqlalchemy import Column, String, Integer, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class AnalysisResult(Base, TimestampMixin):
    """
    Model for storing analysis results.
    
    Attributes:
        id: Unique identifier
        repo_id: Foreign key to repository
        languages: Detected languages with percentages (JSON)
        frameworks: Detected frameworks (JSON)
        issues: Detected legacy issues (JSON)
        tech_debt: Technical debt metrics (JSON)
        total_files: Number of files analyzed
        total_lines: Total lines of code
    """
    
    __tablename__ = "analysis_results"
    
    id = Column(String, primary_key=True)
    repo_id = Column(String, ForeignKey("repositories.id"), nullable=False)
    
    # Analysis data
    languages = Column(JSON, default=list)
    frameworks = Column(JSON, default=list)
    issues = Column(JSON, default=list)
    tech_debt = Column(JSON, default=dict)
    
    # Metrics
    total_files = Column(Integer, default=0)
    total_lines = Column(Integer, default=0)
    
    # Relationship
    repository = relationship("LegacyRepo", back_populates="analyses")
    
    def __repr__(self):
        return f"<AnalysisResult(id={self.id}, repo_id={self.repo_id}, files={self.total_files})>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "repo_id": self.repo_id,
            "languages": self.languages,
            "frameworks": self.frameworks,
            "issues": self.issues,
            "tech_debt": self.tech_debt,
            "total_files": self.total_files,
            "total_lines": self.total_lines,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
