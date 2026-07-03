from enum import Enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ReportStatus(str, Enum):
    UPLOADED = "UPLOADED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class UploadedReport(Base, TimestampMixin):
    __tablename__ = "uploaded_reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    report_type: Mapped[str] = mapped_column(String(80), default="SEARCH_TERM_REPORT", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default=ReportStatus.UPLOADED.value, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
    total_rows: Mapped[int] = mapped_column(default=0, nullable=False)

    owner = relationship("User", back_populates="reports")
    product = relationship("Product", back_populates="reports")

    metrics = relationship("SearchTermMetric", back_populates="report", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="report", cascade="all, delete-orphan")