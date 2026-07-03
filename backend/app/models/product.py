from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(180), nullable=False)
    asin: Mapped[str] = mapped_column(String(20), nullable=False)
    marketplace: Mapped[str] = mapped_column(String(40), default="US", nullable=False)

    selling_price: Mapped[float] = mapped_column(Float, nullable=False)
    profit_margin_percent: Mapped[float] = mapped_column(Float, nullable=False)
    target_acos_percent: Mapped[float] = mapped_column(Float, nullable=False)

    owner = relationship("User", back_populates="products")
    reports = relationship("UploadedReport", back_populates="product", cascade="all, delete-orphan")