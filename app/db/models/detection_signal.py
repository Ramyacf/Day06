import uuid
from datetime import datetime
from sqlalchemy import String, Numeric, Text, DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class DetectionSignal(Base):
    __tablename__ = "detection_signals"
    __table_args__ = (Index("ix_signals_result_type", "analysis_result_id", "signal_type"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_result_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("analysis_results.id", ondelete="CASCADE"), nullable=False)
    signal_type: Mapped[str] = mapped_column(String(100), nullable=False)
    score: Mapped[float | None] = mapped_column(Numeric(7, 4))
    weight: Mapped[float | None] = mapped_column(Numeric(7, 4))
    explanation: Mapped[str | None] = mapped_column(Text)
    evidence_uri: Mapped[str | None] = mapped_column(String(1024))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    result = relationship("AnalysisResult", back_populates="signals")
