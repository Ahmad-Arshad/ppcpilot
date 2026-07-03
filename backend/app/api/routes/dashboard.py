from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.metric import SearchTermMetric
from app.models.recommendation import Recommendation
from app.models.report import UploadedReport
from app.models.user import User
from app.schemas.dashboard import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_reports = (
        db.query(func.count(UploadedReport.id))
        .filter(UploadedReport.owner_id == current_user.id)
        .scalar()
        or 0
    )

    totals = (
        db.query(
            func.coalesce(func.sum(SearchTermMetric.spend), 0),
            func.coalesce(func.sum(SearchTermMetric.sales), 0),
            func.coalesce(func.sum(SearchTermMetric.orders), 0),
        )
        .join(SearchTermMetric.report)
        .filter_by(owner_id=current_user.id)
        .first()
    )

    total_spend = float(totals[0])
    total_sales = float(totals[1])
    total_orders = int(totals[2])

    overall_acos = round((total_spend / total_sales) * 100, 2) if total_sales > 0 else None
    overall_roas = round(total_sales / total_spend, 2) if total_spend > 0 else None

    wasted_spend = (
        db.query(func.coalesce(func.sum(SearchTermMetric.spend), 0))
        .join(SearchTermMetric.report)
        .filter_by(owner_id=current_user.id)
        .filter(SearchTermMetric.sales == 0)
        .scalar()
        or 0
    )

    pending_recommendations = (
        db.query(func.count(Recommendation.id))
        .join(Recommendation.report)
        .filter_by(owner_id=current_user.id)
        .filter(Recommendation.status == "PENDING")
        .scalar()
        or 0
    )

    return DashboardSummary(
        total_reports=total_reports,
        total_spend=round(total_spend, 2),
        total_sales=round(total_sales, 2),
        total_orders=total_orders,
        overall_acos_percent=overall_acos,
        overall_roas=overall_roas,
        wasted_spend=round(float(wasted_spend), 2),
        pending_recommendations=pending_recommendations,
    )