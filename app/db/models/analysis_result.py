import uuid
from datetime import datetime
from sqlalchemy import Numeric, String, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("analysis_runs.id", ondelete="CASCADE"), nullable=False, unique=True)
    verdict: Mapped[str] = mapped_column(String(30), nullable=False)
    risk_score: Mapped[float] = mapped_column(Numeric(7, 4), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Numeric(7, 4), nullable=False)
    language_code: Mapped[str | None] = mapped_column(String(20))
    summary: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    analysis_run = relationship("AnalysisRun", back_populates="result")
    signals = relationship("DetectionSignal", back_populates="result", cascade="all, delete-orphan")
