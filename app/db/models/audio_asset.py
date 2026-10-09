import uuid
from datetime import datetime
from sqlalchemy import String, BigInteger, DateTime, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class AudioAsset(Base):
    __tablename__ = "audio_assets"
    __table_args__ = (
        Index("ix_audio_case_created", "case_id", "created_at"),
        Index("ix_audio_sha256", "sha256"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    s3_bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    original_filename: Mapped[str | None] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    duration_seconds: Mapped[float | None] = mapped_column(nullable=True)
    sample_rate_hz: Mapped[int | None] = mapped_column(nullable=True)
    channels: Mapped[int | None] = mapped_column(nullable=True)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="UPLOADED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    case = relationship("Case", back_populates="audio_assets")
    analysis_runs = relationship("AnalysisRun", back_populates="audio_asset", cascade="all, delete-orphan")
