from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class SearchTermMetric(Base, TimestampMixin):
    __tablename__ = "search_term_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("uploaded_reports.id"), nullable=False)

    campaign_name: Mapped[str] = mapped_column(String(255), nullable=False)
    ad_group_name: Mapped[str] = mapped_column(String(255), nullable=False)
    keyword: Mapped[str | None] = mapped_column(String(255), nullable=True)
    search_term: Mapped[str] = mapped_column(String(255), nullable=False)
    match_type: Mapped[str | None] = mapped_column(String(80), nullable=True)

    impressions: Mapped[int] = mapped_column(default=0, nullable=False)
    clicks: Mapped[int] = mapped_column(default=0, nullable=False)
    spend: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    sales: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    orders: Mapped[int] = mapped_column(default=0, nullable=False)

    acos_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    roas: Mapped[float | None] = mapped_column(Float, nullable=True)
    ctr_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    cpc: Mapped[float | None] = mapped_column(Float, nullable=True)
    conversion_rate_percent: Mapped[float | None] = mapped_column(Float, nullable=True)

    report = relationship("UploadedReport", back_populates="metrics")