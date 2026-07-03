from enum import Enum

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class RecommendationAction(str, Enum):
    MOVE_TO_EXACT = "MOVE_TO_EXACT"
    ADD_NEGATIVE_EXACT = "ADD_NEGATIVE_EXACT"
    REDUCE_BID = "REDUCE_BID"
    INCREASE_BID = "INCREASE_BID"
    MONITOR = "MONITOR"


class RecommendationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXPORTED = "EXPORTED"


class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("uploaded_reports.id"), nullable=False)
    metric_id: Mapped[int] = mapped_column(ForeignKey("search_term_metrics.id"), nullable=False)

    action_type: Mapped[str] = mapped_column(String(80), nullable=False)
    search_term: Mapped[str] = mapped_column(String(255), nullable=False)
    campaign_name: Mapped[str] = mapped_column(String(255), nullable=False)

    reason: Mapped[str] = mapped_column(String(800), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.75, nullable=False)
    status: Mapped[str] = mapped_column(String(40), default=RecommendationStatus.PENDING.value, nullable=False)

    report = relationship("UploadedReport", back_populates="recommendations")