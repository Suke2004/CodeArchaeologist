"""
Repository model for storing analyzed repositories.
"""

from sqlalchemy import Column, String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from .base import Base, TimestampMixin


class RepoStatus(enum.Enum):
    """Status of repository analysis."""
    PENDING = "pending"
    CLONING = "cloning"
    ANALYZING = "analyzing"
    COMPLETE = "complete"
    FAILED = "failed"


class LegacyRepo(Base, TimestampMixin):
    """
    Model for legacy repositories being analyzed.
    
    Attributes:
        id: Unique identifier (UUID)
        url: Repository URL
        name: Repository name
        owner: Repository owner
        user_id: User who submitted the repository
        status: Current processing status
        cloned_at: When repository was cloned
        storage_path: Local path where repo is stored
        metadata: Additional repository metadata (JSON)
    """
    
    __tablename__ = "repositories"
    
    id = Column(String, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    owner = Column(String)
    user_id = Column(String, nullable=False, default="anonymous")
    status = Column(SQLEnum(RepoStatus), default=RepoStatus.PENDING, nullable=False)
    cloned_at = Column(DateTime)
    storage_path = Column(String)
    repo_metadata = Column(JSON, default=dict)  # Renamed from 'metadata' to avoid SQLAlchemy conflict
    
    # Relationship to analysis results
    analyses = relationship("AnalysisResult", back_populates="repository", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<LegacyRepo(id={self.id}, name={self.name}, status={self.status.value})>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "url": self.url,
            "name": self.name,
            "owner": self.owner,
            "user_id": self.user_id,
            "status": self.status.value,
            "cloned_at": self.cloned_at.isoformat() if self.cloned_at else None,
            "storage_path": self.storage_path,
            "metadata": self.repo_metadata,  # Return as 'metadata' for API compatibility
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
