from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.metric import SearchTermMetric
from app.models.user import User
from app.schemas.report import ReportResponse, SearchTermMetricResponse
from app.services.report_service import list_reports, upload_and_process_report

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/upload", response_model=ReportResponse)
async def upload_report(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await upload_and_process_report(db, current_user, product_id, file)


@router.get("", response_model=list[ReportResponse])
def get_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_reports(db, current_user)


@router.get("/{report_id}/metrics", response_model=list[SearchTermMetricResponse])
def get_report_metrics(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(SearchTermMetric)
        .join(SearchTermMetric.report)
        .filter_by(id=report_id, owner_id=current_user.id)
        .order_by(SearchTermMetric.spend.desc())
        .all()
    )